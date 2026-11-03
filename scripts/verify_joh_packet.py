"""Read fixed saved evidence; never import the optimizer, ledger runtime or providers.

Writes only the new JoH packet projection. Native float/exact checkers run on
four explicitly enlarged copies of saved square witnesses, never on caches.
Run from any directory: python3 scripts/verify_joh_packet.py
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import math
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission/joh-20261102/verification"
DRAFT = ROOT / "paper/joh-20261102"
BASE = "07e3cbd3c4855e5e19344885fbf672c3d7a0f039"
inputs = set()


def read(path):
    p = ROOT / path
    inputs.add(p.relative_to(ROOT).as_posix())
    return json.loads(p.read_text())


def rows(campaign):
    out = []
    paths = sorted((ROOT / "campaigns" / campaign).glob("runs*.jsonl"))
    assert paths, f"Missing fixed run files for {campaign}; no run will be launched"
    for p in paths:
        inputs.add(p.relative_to(ROOT).as_posix())
        out.extend(json.loads(line) for line in p.read_text().splitlines() if line.strip())
    assert all("error" not in r for r in out), campaign
    assert len({r['id'] for r in out}) == len(out), campaign
    return out


def p1(a, b):
    return sum(math.comb(a+b, k) for k in range(a, a+b+1)) / 2**(a+b)


def p2(a, b):
    return min(1.0, 2 * min(p1(a, b), p1(b, a)))


def polish(r):
    path = "ledger/polished/" + r['id'].replace('/', '_') + '.json'
    assert (ROOT / path).exists(), f"Missing saved cache {path}; optimization forbidden"
    return read(path)


def value(r, required=False):
    path = ROOT / 'ledger/polished' / (r['id'].replace('/', '_') + '.json')
    return min(r['L'], polish(r)['L']) if required or path.exists() else r['L']


def tol(f, n):
    rec = read(f"catalog/{f}.json")['records'][str(n)]
    return rec['value'], (rec.get('tol') or 1e-5) if rec.get('truncated') else 1e-9


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'base_commit': BASE, 'execution': 'saved-input read-only analysis; no runtime or solver imports', 'checks': {}}
    # Read the saved event export as data. Do not instantiate ActiveGraph.
    objects = {}
    ep = ROOT/'ledger/events.jsonl'
    inputs.add('ledger/events.jsonl')
    for line in ep.open():
        e = json.loads(line)
        if e['type'] == 'object.created':
            o = e['payload']['object']
            objects[o['id']] = {'type': o['type'], **o['data']}
        elif e['type'] == 'patch.applied':
            p = e['payload']['patch']
            assert p['op'] == 'update', p['op']
            objects[p['target']].update(p['value'])
    cells = {o['cell']: o for o in objects.values() if o['type'] == 'cell'}
    solved = defaultdict(bool)
    for o in objects.values():
        if o['type'] == 'candidate' and o.get('verdict') in ('matches record', 'below record'):
            solved[o['cell']] = True
    c7 = {(c['family'], c['n'], c['method']): solved[k] for k,c in cells.items() if c['campaign']=='C07-breadth-best'}
    c10 = {(c['family'], c['n']): solved[k] for k,c in cells.items() if c['campaign']=='C10-portfolio'}
    pairs=[]
    for f,n in sorted(c10):
        r=c7[(f,n,'rigid-best')]
        pairs.append((r or c7[(f,n,'harden-best')], r or c10[(f,n)], r or c7[(f,n,'grow-best')]))
    a=sum(x and not y for x,y,_ in pairs); b=sum(y and not x for x,y,_ in pairs)
    got={'rigid64':sum(y for x,y,z in pairs),'rigid32+harden32':sum(x for x,y,z in pairs),'rigid32+grow32':sum(z for x,y,z in pairs),'mixed_only':a,'rigid64_only':b,'p':p2(a,b)}
    assert got==read('analysis/C10-portfolio.json'), (got, read('analysis/C10-portfolio.json'))
    report['checks']['C10']={**got,'instances':len(pairs),'registered_one_sided_p':p1(a,b),'source':'saved event object/patch data, no event replay runtime'}
    r15=rows('C15-heldout-decision')
    by15={(r['family'],r['n'],r['method'],r['seed']):r for r in r15}
    inst=sorted({(r['family'],r['n']) for r in r15})
    saved=read('analysis/C15.json'); results={}; lower=[0,0,0]
    for f,n in inst:
        H=[by15[f,n,'harden-best',s] for s in range(1,65)]
        R=[by15[f,n,'rigid-best',s] for s in range(1,65)]
        pick='harden' if min(r['L'] for r in H[:8])<min(r['L'] for r in R[:8]) else 'rigid'
        pilot=H[:8]+R[:8]+(H if pick=='harden' else R)[8:56]
        result={}
        for name,pool in [('always-rigid',R),('always-harden',H),('pilot',pilot)]:
            chosen=min(pool,key=lambda r:r['L'])
            L=value(chosen,required=True); rec,t=tol(f,n)
            result[name]={'run':chosen['id'],'L':L,'reached':L<=rec+t}
            s=saved['instances'][f'{f}/n{n}'][name]
            assert result[name]['run']==s['run'] and abs(L-s['L'])<1e-12 and result[name]['reached']==s['reached'], (f,n,name)
        x,y=result['pilot']['L'],result['always-rigid']['L']
        lower[0 if x<y*(1-1e-9) else 1 if y<x*(1-1e-9) else 2]+=1
        results[f'{f}/n{n}']={'pick':pick,**result}
    pv={'a_lower':lower[0],'b_lower':lower[1],'ties':lower[2],'p':p2(*lower[:2])}
    assert pv==saved['pilot_vs_rigid'], pv
    report['checks']['C15']={'instances':len(inst),'raw_rows':len(r15),'pilot_vs_rigid':pv,'reached':saved['reached'],'cache_misses':0,'smoke_test_note':read('campaigns/C15-heldout-decision/plan.json')['pre_registration_note']}
    (OUT/'C15-policy-crosswalk.json').write_text(json.dumps(results,indent=2)+'\n')
    r16=rows('C16-squares-long'); r9=rows('C09-budget')
    index9={r['id']:r for r in r9}
    repeated=[]
    for r in r16:
        if r['n'] in {19,28,29} and r['method'] in {'harden-best','rigid-best'}:
            old=index9[r['id']]
            for k in ['L','Lsoft','poses','evals','steps']:assert r[k]==old[k],(r['id'],k)
            repeated.append(r['id'])
    groups=defaultdict(list)
    for r in r16:groups[r['n'],r['method']].append(r)
    counts=[0,0,0]
    for n in sorted({r['n'] for r in r16}-{19,28,29}):
        x=min(value(r) for r in groups[n,'harden-best']);y=min(value(r) for r in groups[n,'rigid-best'])
        counts[0 if x<y*(1-1e-9) else 1 if y<x*(1-1e-9) else 2]+=1
    c16={'a_lower':counts[0],'b_lower':counts[1],'ties':counts[2],'p_lower':p2(*counts[:2])}
    previous=read('analysis/ablations.json')['C16-squares-long']['harden_vs_rigid_new_only']
    assert all(c16[k]==previous[k] for k in c16),(c16,previous)
    report['checks']['C16']={'raw_rows':len(r16),'reused_harden_rigid_rows':len(repeated),'reused_instances':[19,28,29],'new_only_instances':sum(counts),'new_only':c16,'reused_run_ids':repeated}
    # Exact tests of deliberately enlarged, saved square witnesses. No optimizer.
    r7=rows('C07-breadth-best'); witness=[]
    # Recompute C14 only from its committed top-three cache and original
    # event-export candidate values. A missing file fails; no cache creation.
    plan14=read('campaigns/C14-equal-refine/plan.json')
    wanted={(x['family'],n) for x in plan14['instances'] for n in x['ns']}
    g7=defaultdict(list)
    for r in r7:
        if (r['family'],r['n']) in wanted:g7[r['family'],r['n'],r['method'].replace('-best','')].append(r)
    treatments={'raw':{},'equal_top3':{},'c07_policy':{}}
    for key,pool in g7.items():
        f,n,m=key
        raw=min(r['L'] for r in pool)
        top=sorted(pool,key=lambda r:r['L'])[:3]
        eq=min([raw]+[read('campaigns/C14-equal-refine/tightened/'+r['id'].replace('/','_')+'.json')['L'] for r in top])
        cell=next(c for c in cells.values() if c['campaign']=='C07-breadth-best' and c['family']==f and c['n']==n and c['method']==m+'-best')
        original=[o['L_polished'] for o in objects.values() if o['type']=='candidate' and o.get('cell')==cell['cell'] and o.get('L_polished') is not None]
        treatments['raw'][key]=raw;treatments['equal_top3'][key]=eq;treatments['c07_policy'][key]=min([raw]+original)
    counts14={}
    for name,vals in treatments.items():
        c={m:0 for m in ['harden','grow','rigid','sa','pc']}
        for f,n in wanted:
            lo=min(vals[f,n,m] for m in c)
            for m in c:c[m]+=vals[f,n,m]<=lo*(1+1e-9)+1e-12
        counts14[name]=c
    expected14=read('analysis/C14.json')
    assert all(counts14[k]==expected14[k] for k in counts14),(counts14,expected14)
    report['checks']['C14']={'instances':len(wanted),'counts':counts14,'optimization_calls':0}
    for n,source in [(11,r7),(19,r7),(17,r16),(26,r16)]:
        candidates=[r for r in source if r['family']=='squ-in-squ' and r['n']==n and r['method']=='harden-best']
        chosen=min(candidates,key=value); cached=polish(chosen)
        original=min(chosen['L'],cached['L'])
        poses=cached['poses'] if cached['L']<=chosen['L'] else chosen['poses']
        bound=original*1.00001+1e-6
        claim={'problem':'saved-study witness, deliberately enlarged container; not a new record','piece':'square','container':'square','s_full':bound,'pieces':[[x*1.000001,y*1.000001,t] for x,y,t in poses]}
        wp=OUT/f'witness-n{n}.json';wp.write_text(json.dumps(claim,indent=2)+'\n')
        logs={}
        for name,cmd in [('float',[sys.executable,'verify.py',str(wp)]),('exact',[sys.executable,'-m','packing.certify',str(wp)])]:
            p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=30)
            (OUT/f'witness-n{n}-{name}.txt').write_text(p.stdout+p.stderr)
            assert p.returncode==0,(name,n,p.stdout,p.stderr)
            logs[name]='PASS'
        witness.append({'n':n,'source_campaign':chosen['campaign'],'run':chosen['id'],'stored_objective':original,'certified_enlarged_bound':bound,'center_factor':1.000001,'bound_factor':1.00001,'bound_addition':1e-6,'not_a_certificate_at_stored_objective':True,'checks':logs})
    report['checks']['selected_witnesses']=witness
    # Generate new SI tables only; native generated paper tables are preserved.
    tuning=[]
    plan=read('campaigns/C06-tune-best/plan.json')
    for m in plan['methods']:
        selected=read(f'methods/{m}-best.json');grid=plan['configs'][m]
        row={'method':m,'configs':len(grid),'selected':selected['params'],'ranges':{},'boundary':{}}
        for k,v in selected['params'].items():
            values=sorted({c['params'][k] for c in grid});row['ranges'][k]=values;row['boundary'][k]=v in (values[0],values[-1])
        tuning.append(row)
    report['checks']['C06_grid']=tuning
    ev=[r'\begin{tabular}{lrrr}\toprule',r'comparison & first lower/only & second lower/only & two-sided $p$\\\midrule',
        f"C10 mixed vs doubled rigid (solved) & {a} & {b} & {p2(a,b):g}\\\\",
        f"C15 pilot vs rigid (size) & {lower[0]} & {lower[1]} & {p2(*lower[:2]):g}\\\\",
        f"C16 new-only harden vs rigid (size) & {counts[0]} & {counts[1]} & {p2(*counts[:2]):g}\\\\",r'\bottomrule\end{tabular}']
    (DRAFT/'evidence-summary.tex').write_text('\n'.join(ev)+'\n')
    (DRAFT/'evidence-macros.tex').write_text(r'\newcommand{\CtenRegisteredP}{'+f'{p1(a,b):g}'+'}\n')
    wtex=[r'\begin{tabular}{rrr}\toprule',r'$n$ & stored contact objective & checked enlarged side\\\midrule']
    for w in witness:
        wtex.append(f"{w['n']} & {w['stored_objective']:.10f} & {w['certified_enlarged_bound']:.10f}\\\\")
    wtex.append(r'\bottomrule\end{tabular}')
    (DRAFT/'witness-summary.tex').write_text('\n'.join(wtex)+'\n')
    ttex=[r'\begin{tabular}{lp{0.38\linewidth}l}\toprule',r'method & selected parameters & grid boundary\\\midrule']
    for t in tuning:
        symbols={'mu':r'$\mu$', 'noiseScale':r'$\nu$', 'gamma0':r'$\gamma_0$', 'saT0':r'$T_0$', 'pcKick':'kick', 'pcRelax':'relax steps'}
        params=', '.join(symbols[k]+'='+str(v) for k,v in t['selected'].items())
        ttex.append(t['method']+' & '+params+' & '+('both' if all(t['boundary'].values()) else 'partial')+r'\\')
    ttex.append(r'\bottomrule\end{tabular}')
    (DRAFT/'tuning-summary.tex').write_text('\n'.join(ttex)+'\n')
    # Journal-only caption adaptation: preserve every generated numerical row.
    # Original paper/tables/C05-cubes.tex is read, never written.
    original_table=ROOT/'paper/tables/C05-cubes.tex'
    inputs.add('paper/tables/C05-cubes.tex')
    text=original_table.read_text()
    text=text.replace('best known','reference')
    text=text.replace('record budget','prior search budget')
    text=text.replace('our earlier $n=12$ record','the prior reported $n=12$ feasible bound')
    text=text.replace('which these runs try to reproduce','from a separate 192-start search; this is not a current-study catalogue target')
    (DRAFT/'tables/C05-cubes.tex').write_text(text)
    inputs.update(['packing/certify.py','verify.py','packing/ledger.py','packing/decision.py','packing/ablations.py','packing/polish.py','packing/refine.py','packing/stats.py','packing/analyze.py','analysis/C14.json','analysis/stats.json','analysis/reference_budget.json'])
    manifest={'source_commit':BASE,'purpose':'fixed evidence used by bounded journal verification; saved code not executed unless identified','files':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),'bytes':(ROOT/p).stat().st_size} for p in sorted(inputs)]}
    (OUT/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    report['input_files']=len(manifest['files']); report['status']='PASS'
    report['scope_limits']=['Not exhaustive raw-data reproduction of all campaigns','No certification at the original contact objective','No pentagon/octagon exact certification','No canonical ledger runtime, optimizer, provider or service invoked']
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':list(report['checks']),'input_files':report['input_files'],'report':str(OUT/'report.json')},indent=2))


if __name__=='__main__':
    main()
