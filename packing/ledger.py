"""The research ledger: an ActiveGraph event store that records what was planned, run, polished,
certified and concluded, and reacts to it.

    python -m packing.ledger ingest <campaign-id>        # plan + new results -> events; behaviors fire
    python -m packing.ledger finding "<text>" --evidence <cell or campaign id> ... [--campaign C]
    python -m packing.ledger close <campaign-id> "<decision taken>"
    python -m packing.ledger export                      # ledger/events.jsonl (committed)

Raw runs stay in campaigns/<C>/runs*.jsonl. The ledger stores, per ingested file, its SHA-256 and
per-cell statistics (a cell is campaign x family x n x method x budget x config), plus an object
for every run sent to exact tightening, every polish result, every certificate, claim and finding.

Behaviors (reactive, in this order of causation):
  summarize   runs.ingested     -> cell objects; candidate objects; polish.requested
  polisher    polish.requested  -> exact tightening (packing.tighten) -> polish.completed
  judge       polish.completed  -> 'matches record' / 'below record' -> certify.requested
  certifier   certify.requested -> claim folder + verify + exact certificate -> certify.passed|failed
  recorder    finding.recorded / campaign.closed -> finding and decision objects with evidence edges
"""
import argparse, glob, hashlib, json, os, statistics, sys, time
import activegraph as ag
from activegraph import Graph, Runtime, behavior, Event

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB = os.path.join(ROOT, 'ledger', 'ledger.sqlite')
POLISH_TOP = 3          # per cell, the best runs sent to tightening ...
POLISH_REL = 0.02       # ... if within 2% of the best known value
POLISH_CAP = 10         # at most this many tightenings per cell
POLISH_GAP = 2e-3       # ... plus every run within this of the best known value
MATCH_TOL = 1e-9        # tightened size within this of the record = "matches"


def catalog(fam):
    return json.load(open(os.path.join(ROOT, 'catalog', fam + '.json')))


def _key(*parts):
    return '/'.join(str(p) for p in parts)


def build_behaviors(H):
    """Behaviors read the full graph H['G'] (set after loading) and write through the behavior graph."""

    def find(type_, **where):
        objs = H['G'].objects(type_, where=where)
        return objs[0] if objs else None

    @behavior(name='plan', on=['campaign.planned'])
    def plan(event, graph, ctx):
        p = event.payload
        if not find('campaign', cid=p['id']):
            graph.add_object('campaign', {'cid': p['id'], 'title': p['title'], 'question': p['question'],
                                          'hypothesis': p.get('hypothesis'), 'decision_rule': p['decision_rule'],
                                          'created': p.get('created'), 'status': 'planned'})

    @behavior(name='summarize', on=['runs.ingested'])
    def summarize(event, graph, ctx):
        p = event.payload
        camp = find('campaign', cid=p['campaign'])
        for c in p['cells']:
            key = c['cell']
            prev = find('cell', cell=key)
            if prev:
                graph.patch_object(prev.id, c)
                cell_id = prev.id
            else:
                o = graph.add_object('cell', c)
                cell_id = o.id
                if camp:
                    graph.add_relation(cell_id, camp.id, 'in_campaign')
            for cand in c.get('candidates', []):
                if find('candidate', run=cand['run']):
                    continue
                co = graph.add_object('candidate', dict(cand, cell=key, status='queued'))
                graph.add_relation(co.id, cell_id, 'from_cell')
                graph.emit('polish.requested', {'candidate': co.id, 'run': cand['run'], 'file': cand['file']})
        if camp:
            graph.patch_object(camp.id, {'status': 'running' if not p.get('complete') else 'complete'})

    @behavior(name='polisher', on=['polish.requested'])
    def polisher(event, graph, ctx):
        from . import tighten
        p = event.payload
        cached = os.path.join(ROOT, 'ledger', 'polished', p['run'].replace('/', '_') + '.json')
        row = None
        for line in open(os.path.join(ROOT, p['file'])):
            if p['run'] in line:
                r = json.loads(line)
                if r['id'] == p['run']:
                    row = r
                    break
        F = catalog(row['family'])
        t0 = time.time()
        if os.path.exists(cached):  # computed by packing.polish (same function, same input)
            out = json.load(open(cached))
        else:
            try:
                out = tighten.solve(F['piece'], F['container'], row['poses'])
            except Exception as e:
                graph.emit('polish.failed', {'candidate': p['candidate'], 'error': repr(e)})
                return
        rec = F['records'].get(str(row['n']))
        gap = out['L'] - rec['value'] if rec else None
        os.makedirs(os.path.join(ROOT, 'ledger', 'polished'), exist_ok=True)
        fn = os.path.relpath(cached, ROOT)
        if not os.path.exists(cached):
            json.dump({'run': row['id'], 'family': row['family'], 'n': row['n'], 'L': out['L'], 'L_raw': row['L'],
                       'poses': out['poses'], 'history': out['history']}, open(cached, 'w'))
        graph.patch_object(p['candidate'], {'status': 'polished', 'L_polished': out['L'], 'gap_polished': gap})
        graph.emit('polish.completed', {'candidate': p['candidate'], 'run': row['id'], 'family': row['family'], 'n': row['n'],
                                        'L': out['L'], 'gap': gap, 'record': rec['value'] if rec else None,
                                        'truncated': rec.get('truncated') if rec else None, 'file': fn,
                                        'seconds': round(time.time() - t0, 2)})

    @behavior(name='judge', on=['polish.completed'])
    def judge(event, graph, ctx):
        p = event.payload
        if p['gap'] is None:
            return
        # a truncated catalogue value v+ means the record lies in [v, v + 10^-d); below v is new
        if p['gap'] < -MATCH_TOL:
            graph.patch_object(p['candidate'], {'verdict': 'below record'})
            graph.emit('certify.requested', dict(p))
        elif abs(p['gap']) <= MATCH_TOL or (p.get('truncated') and p['gap'] < 1e-5):
            graph.patch_object(p['candidate'], {'verdict': 'matches record'})
        else:
            graph.patch_object(p['candidate'], {'verdict': 'above record'})

    @behavior(name='certifier', on=['certify.requested'])
    def certifier(event, graph, ctx):
        from . import claims
        p = event.payload
        res = claims.make_claim(p['family'], p['n'], os.path.join(ROOT, p['file']))
        if res['ok']:
            o = graph.add_object('claim', {'family': p['family'], 'n': p['n'], 's_full': res['s_full'], 'record': p['record'],
                                           'improvement': p['record'] - res['s_full'], 'folder': res['folder']})
            graph.add_relation(o.id, p['candidate'], 'certifies')
            graph.emit('certify.passed', {'claim': o.id, **{k: res[k] for k in ('family', 'n', 's_full', 'folder')}})
        else:
            graph.emit('certify.failed', {'candidate': p['candidate'], 'reason': res.get('reason')})

    @behavior(name='recorder', on=['finding.recorded', 'campaign.closed'])
    def recorder(event, graph, ctx):
        p = event.payload
        if event.type == 'finding.recorded':
            o = graph.add_object('finding', {'text': p['text'], 'campaign': p.get('campaign'), 'date': p.get('date'), 'evidence': p.get('evidence', [])})
            for ev in p.get('evidence', []):
                tgt = find('cell', cell=ev) or find('campaign', cid=ev) or find('claim', folder=ev)
                if tgt:
                    graph.add_relation(o.id, tgt.id, 'supported_by')
        else:
            camp = find('campaign', cid=p['campaign'])
            if camp:
                graph.patch_object(camp.id, {'status': 'closed', 'decision': p['decision'], 'closed': p.get('date')})

    return [plan, summarize, polisher, judge, certifier, recorder]


def open_ledger():
    ag.clear_registry()
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    H = {}
    if os.path.exists(DB):
        rt = Runtime.load(DB, behaviors=build_behaviors(H))
    else:
        rt = Runtime(Graph(), behaviors=build_behaviors(H), persist_to=DB)
    H['G'] = rt.graph
    return rt, rt.graph


def emit(G, type_, payload):
    G.emit(Event(id=G.ids.event(), type=type_, payload=payload))


def _cells(campaign, rows, files, polish=True):
    by = {}
    for r in rows:
        if 'error' in r:
            continue
        by.setdefault(_key(campaign, r['family'], 'n%d' % r['n'], r['method'], 'B%s' % r['budget'], r['config']), []).append(r)
    cells = []
    for key, rs in sorted(by.items()):
        rs.sort(key=lambda r: r['L'])
        gaps = [r['gap'] for r in rs if r['gap'] is not None]
        r0 = rs[0]
        cand = []
        for i, r in enumerate(rs):
            rel = r['gap'] / r['record'] if r.get('record') else 0
            if polish and len(cand) < POLISH_CAP and ((i < POLISH_TOP and rel < POLISH_REL) or (r['gap'] is not None and r['gap'] < POLISH_GAP)):
                cand.append({'run': r['id'], 'file': files[r['id']], 'L_raw': r['L'], 'gap_raw': r['gap']})
        cells.append({'cell': key, 'campaign': campaign, 'family': r0['family'], 'n': r0['n'], 'method': r0['method'],
                      'budget': r0['budget'], 'config': r0['config'], 'runs': len(rs), 'record': r0.get('record'),
                      'best_L': rs[0]['L'], 'best_run': rs[0]['id'], 'best_gap': rs[0]['gap'],
                      'median_gap': statistics.median(gaps) if gaps else None,
                      'hits_1e3': sum(g < 1e-3 for g in gaps), 'hits_1e4': sum(g < 1e-4 for g in gaps),
                      'ms_mean': round(statistics.mean(r['ms'] for r in rs), 1),
                      'evals_mean': round(statistics.mean(r['evals'] for r in rs)), 'candidates': cand})
    return cells


def ingest(campaign):
    rt, G = open_ledger()
    cdir = os.path.join(ROOT, 'campaigns', campaign)
    plan = json.load(open(os.path.join(cdir, 'plan.json')))
    if not G.objects('campaign', where={'cid': campaign}):
        emit(G, 'campaign.planned', {k: plan.get(k) for k in ('id', 'title', 'question', 'hypothesis', 'decision_rule', 'created')}
             | {'plan_sha256': hashlib.sha256(open(os.path.join(cdir, 'plan.json'), 'rb').read()).hexdigest()})
        rt.run_until_idle()
    rows, files, digests = [], {}, {}
    for f in sorted(glob.glob(os.path.join(cdir, 'runs*.jsonl'))):
        rel = os.path.relpath(f, ROOT)
        data = open(f, 'rb').read()
        digests[rel] = hashlib.sha256(data).hexdigest()
        for line in data.decode().splitlines():
            if line.strip():
                r = json.loads(line)
                rows.append(r)
                files[r['id']] = rel
    errors = [r for r in rows if 'error' in r]
    emit(G, 'runs.ingested', {'campaign': campaign, 'files': digests, 'runs': len(rows), 'errors': len(errors),
                              'error_ids': [r['id'] for r in errors][:50], 'cells': _cells(campaign, rows, files, plan.get('polish', True))})
    rt.run_until_idle()
    print(f'ingested {campaign}: {len(rows)} runs, {len(errors)} errors; ledger has {len(G.events)} events')


def finding(text, evidence, campaign=None):
    rt, G = open_ledger()
    emit(G, 'finding.recorded', {'text': text, 'evidence': evidence, 'campaign': campaign, 'date': time.strftime('%Y-%m-%d')})
    rt.run_until_idle()


def close(campaign, decision):
    rt, G = open_ledger()
    emit(G, 'campaign.closed', {'campaign': campaign, 'decision': decision, 'date': time.strftime('%Y-%m-%d')})
    rt.run_until_idle()


def export():
    rt, G = open_ledger()
    out = os.path.join(ROOT, 'ledger', 'events.jsonl')
    rt.export_trace(out)
    print('exported', len(G.events), 'events to', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    a = sub.add_parser('ingest'); a.add_argument('campaign')
    a = sub.add_parser('finding'); a.add_argument('text'); a.add_argument('--evidence', nargs='*', default=[]); a.add_argument('--campaign')
    a = sub.add_parser('close'); a.add_argument('campaign'); a.add_argument('decision')
    sub.add_parser('export')
    args = ap.parse_args()
    if args.cmd == 'ingest':
        ingest(args.campaign)
    elif args.cmd == 'finding':
        finding(args.text, args.evidence, args.campaign)
    elif args.cmd == 'close':
        close(args.campaign, args.decision)
    elif args.cmd == 'export':
        export()
    else:
        ap.print_help()
