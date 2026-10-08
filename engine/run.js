#!/usr/bin/env node
// Campaign runner. Usage: node engine/run.js campaigns/<C>/plan.json [--worker k --of m]
// Expands the plan into jobs (instance × method × budget × seed × config), skips jobs already in
// any runs*.jsonl of the campaign, and appends one JSON line per finished run to runs-w<k>.jsonl.
// Keeps, per instance × method × config, the replay of the best run so far, plus up to 5 hits.
'use strict';
const fs = require('fs'), path = require('path');
const E2 = require('./engine2d.js');

const args = process.argv.slice(2);
const planPath = args[0];
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const worker = +opt('worker', 0), of = +opt('of', 1), limit = +opt('limit', Infinity);
const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const dir = path.dirname(planPath), root = path.join(dir, '..', '..');
const catalog = {};
const fam = (f) => catalog[f] || (catalog[f] = JSON.parse(fs.readFileSync(path.join(root, 'catalog', f + '.json'), 'utf8')));
const methodsDir = path.join(root, 'methods');
const methodCfg = (m) => { const p = path.join(methodsDir, m + '.json'); return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : { method: m }; };

// ---- expand jobs ----
const jobs = [];
for (const inst of plan.instances) for (const n of inst.ns) for (const m of plan.methods) for (const B of plan.budgets) {
  const configs = (plan.configs && (plan.configs[m] || plan.configs['*'])) || [{ name: 'default' }];
  for (const cf of configs) for (const seed of seedList(plan.seeds)) {
    const id = `${inst.family}/n${n}/${m}/B${B}/${cf.name}/s${seed}`;
    jobs.push({ id, family: inst.family, n, method: m, budget: B, config: cf, seed });
  }
}
function seedList(s) { return Array.isArray(s) ? s : Array.from({ length: s }, (_, i) => i + 1); }

// ---- done set ----
const done = new Set();
for (const f of fs.readdirSync(dir)) if (/^runs.*\.jsonl$/.test(f)) {
  for (const line of fs.readFileSync(path.join(dir, f), 'utf8').split('\n')) if (line.trim()) { try { done.add(JSON.parse(line).id); } catch (e) { } }
}
const mine = jobs.filter((j, i) => i % of === worker && !done.has(j.id));
console.error(`[${plan.id} w${worker}/${of}] ${jobs.length} jobs, ${done.size} done, ${mine.length} to run`);

const outPath = path.join(dir, `runs-w${worker}.jsonl`);
const repDir = path.join(dir, 'replays'); fs.mkdirSync(repDir, { recursive: true });
const bestFile = (j) => path.join(repDir, `${j.family}_n${j.n}_${j.method}_B${j.budget}_${j.config.name}.json`.replace(/\//g, '-'));
const round = (x, d) => +x.toFixed(d);

let count = 0;
for (const j of mine) {
  if (count >= limit) break;
  const F = fam(j.family), rec = F.records[String(j.n)];
  const mc = methodCfg(j.method);
  const cfg = Object.assign({}, mc.params || {}, plan.overrides || {}, j.config.params || {},
    { n: j.n, piece: F.piece, container: F.container, method: mc.method || j.method, seed: j.seed, budget: j.budget });
  let res, err = null;
  try { res = E2.run(cfg); } catch (e) { err = String(e && e.stack || e); }
  const row = { id: j.id, campaign: plan.id, family: j.family, n: j.n, method: j.method, budget: j.budget, config: j.config.name, seed: j.seed, t: new Date().toISOString() };
  if (err) { row.error = err; }
  else {
    row.L = res.L; row.Lsoft = round(res.Lsoft, 6); row.record = rec ? rec.value : null;
    row.gap = rec ? res.L - rec.value : null;
    row.ms = res.ms; row.evals = res.evals; row.steps = res.steps;
    row.poses = res.poses.map(p => [round(p[0], 10), round(p[1], 10), round(p[2], 10)]);
    // replays: best so far for this instance × method × budget × config, and up to 5 hits
    const bf = bestFile(j);
    let prev = null; try { prev = JSON.parse(fs.readFileSync(bf, 'utf8')); } catch (e) { }
    const replay = { id: j.id, family: j.family, piece: F.piece, container: F.container, n: j.n, method: j.method, seed: j.seed, L: res.L, record: row.record, frames: res.frames };
    if (!prev || res.L < prev.L) fs.writeFileSync(bf, JSON.stringify(replay));
    if (rec && row.gap < 1e-3) {
      const hd = path.join(repDir, 'hits'); fs.mkdirSync(hd, { recursive: true });
      const pre = `${j.family}_n${j.n}_${j.method}`, have = fs.readdirSync(hd).filter(f => f.startsWith(pre + '_')).length;
      if (have < 5) fs.writeFileSync(path.join(hd, `${pre}_B${j.budget}_${j.config.name}_s${j.seed}.json`), JSON.stringify(replay));
    }
  }
  fs.appendFileSync(outPath, JSON.stringify(row) + '\n');
  count++;
  if (count % 50 === 0) console.error(`[${plan.id} w${worker}] ${count}/${mine.length}`);
}
console.error(`[${plan.id} w${worker}] finished ${count}`);
