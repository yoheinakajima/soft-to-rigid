// The pair-evaluation budget given to sa and pc: one hardening run (seed 999999) with the baseline's own pressure and
// noise settings, as engine2d.matchedEvals computes it. Writes analysis/reference_budget.json for squares in a square.
//   node scripts/reference_budget.js
const path = require('path'), fs = require('fs');
const E = require(path.join(__dirname, '..', 'engine', 'engine2d.js'));
const out = {};
for (const m of ['sa-best', 'pc-best']) {
  const params = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'methods', m + '.json'))).params;
  for (const n of [20, 30]) {
    const c = Object.assign({}, E.DEFAULTS, params, { piece: 'square', container: 'square', n, budget: 1, method: 'harden', seed: 999999, frames: 2 });
    out[`${m}/n${n}`] = E.run(c).evals;
  }
}
fs.writeFileSync(path.join(__dirname, '..', 'analysis', 'reference_budget.json'), JSON.stringify(out, null, 1));
console.log(out);
