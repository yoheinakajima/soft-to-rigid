"""Journal-only arithmetic/plots from fixed saved files; no native module imports.
No optimization, solver, provider or ledger runtime. Baseline files never written.
"""
from pathlib import Path
from collections import defaultdict
import json, math, hashlib
R=Path(__file__).resolve().parents[1]
O=R/'submission/joh-20261102/verification'
J=R/'paper/joh-20261102'
inputs={}
def read(s):
 p=R/s;inputs[s]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def tail(a,b):
 return sum(math.comb(a+b,k)for k in range(a,a+b+1))/2**(a+b)
def two(a,b):return min(1.,2*min(tail(a,b),tail(b,a)))
def fmt(p):return f'{p:.6g}'
checks=[]
def add(c,comparison,endpoint,a,b,sides,scope,decision=None,registered=True):
 p=tail(a,b)if sides==1 else two(a,b)
 checks.append(dict(campaign=c,comparison=comparison,endpoint=endpoint,a=a,b=b,sides=sides,registered_p=p if registered else None,two_sided_p=two(a,b),scope=scope,decision=decision or ('direction supported'if p<.05 and a>b else 'opposite direction'if p<.05 and b>a else 'not detected')))
 assert two(a,b)<=2*tail(a,b)+1e-15 and two(a,b)<=2*tail(b,a)+1e-15
for c in ['C04-breadth','C07-breadth-best']:
 read(f'campaigns/{c}/plan.json');saved=read(f'analysis/{c}.json')
 for m,q in saved['sign_tests'].items():
  a,b=q['harden_only'],q['other_only'];assert abs(tail(a,b)-q['p_harden_better'])<1e-14
  add(c[:3],f'H vs {m}','reached',a,b,1,'pooled, H greater')
# Reconstruct both named C10 portfolios from event-export objects; no event runtime.
p=R/'ledger/events.jsonl';inputs['ledger/events.jsonl']=hashlib.sha256(p.read_bytes()).hexdigest();objects={}
for line in p.open():
 e=json.loads(line)
 if e['type']=='object.created':
  o=e['payload']['object'];objects[o['id']]={'type':o['type'],**o['data']}
 elif e['type']=='patch.applied':
  q=e['payload']['patch'];assert q['op']=='update';objects[q['target']].update(q['value'])
solved=defaultdict(bool)
for o in objects.values():
 if o['type']=='candidate'and o.get('verdict')in('matches record','below record'):solved[o['cell']]=True
cells={o['cell']:o for o in objects.values()if o['type']=='cell'}
c7={(c['family'],c['n'],c['method']):solved[k]for k,c in cells.items()if c['campaign']=='C07-breadth-best'}
c10={(c['family'],c['n']):solved[k]for k,c in cells.items()if c['campaign']=='C10-portfolio'}
read('campaigns/C10-portfolio/plan.json')
for m in ['harden','grow']:
 pairs=[(c7[f,n,'rigid-best']or c7[f,n,m+'-best'],c7[f,n,'rigid-best']or c10[f,n])for f,n in c10]
 a=sum(x and not y for x,y in pairs);b=sum(y and not x for x,y in pairs)
 add('C10','R+H vs R64'if m=='harden'else'R+G vs R64','reached',a,b,1,'mixed greater')
abl=read('analysis/ablations.json')
for c,m in [('C11-snap','snap'),('C12-grow-area','grow-area')]:
 read(f'campaigns/{c}/plan.json')
 for f,q in abl[c]['families'].items():
  v=q['harden_vs_'+m];add(c[:3],f'H vs {m}','reached',v['a_only_reached'],v['b_only_reached'],2,f)
read('campaigns/C13-budget-clean/plan.json')
for name,q in abl['C13-budget-clean'].items():
 if isinstance(q,dict):add('C13',name.replace('_',' '),'size',q['a_lower'],q['b_lower'],2,'28 fixed instances',registered=not name.endswith('vs_base'))
read('campaigns/C15-heldout-decision/plan.json');d=read('analysis/C15.json');q=d['pilot_vs_rigid'];add('C15','pilot vs rigid','size',q['a_lower'],q['b_lower'],2,'60 held-out, smoke tests')
read('campaigns/C16-squares-long/plan.json');q=abl['C16-squares-long']['harden_vs_rigid'];add('C16','H vs R, all','size',q['a_lower'],q['b_lower'],2,'14 targeted; 3 reused')
q=abl['C16-squares-long']['harden_vs_rigid_new_only'];add('C16','H vs R, new only','size',q['a_lower'],q['b_lower'],2,'11; descriptive exclusion',registered=False)
# No inference over a random benchmark population or multiplicity adjustment implied.
(O/'registered-tests.json').write_text(json.dumps({'basis':'fixed saved counts and plans; exact combinatorics, not new runs','tests':checks},indent=2)+'\n')
tex=[r'\scriptsize',r'\begin{longtable}{lllrllll}',r'\caption{Plan-specified sign comparisons and descriptive two-sided values. H: hardening; R: rigid; G: grow. Counts are first versus second discordants.}\label{tab:registered}\\',r'\toprule campaign & comparison/scope & endpoint & counts & sides & registered $p$ & $p_2$ & result\\\midrule\endfirsthead',r'\toprule campaign & comparison/scope & endpoint & counts & sides & registered $p$ & $p_2$ & result\\\midrule\endhead']
for q in checks:
 label=q['comparison']
 if q['campaign']in['C11','C12']:label=q['scope']
 label=label.replace('harden','H').replace('rigid','R').replace('longer vs','long vs').replace('squ-in-','sq/').replace('tri-in-','tri/').replace('hex-in-','hex/').replace('cir-in-','disk/')
 tex.append(f"{q['campaign']} & {label} & {q['endpoint']} & {q['a']}:{q['b']} & {q['sides']} & {fmt(q['registered_p']) if q['registered_p'] is not None else '--'} & {fmt(q['two_sided_p'])} & "+('first'if (q['registered_p'] if q['registered_p'] is not None else q['two_sided_p'])<.05 and q['a']>q['b']else'second'if (q['registered_p'] if q['registered_p'] is not None else q['two_sided_p'])<.05 and q['b']>q['a']else'ND')+r'\\')
tex+=[r'\bottomrule\end{longtable}',r'\normalsize']
(J/'registered-tests.tex').write_text('\n'.join(tex)+'\n')
stats=read('analysis/stats.json');refs=read('analysis/reference_budget.json');diag=[]
for m in ['sa','pc']:
 for n in[20,30]:
  evals=stats['diagnostics']['per_run'][f'{m}/n{n}']['pair_evals'];ref=refs[f'{m}-best/n{n}'];diag.append(dict(method=m,n=n,mean_pair_evals=evals,reference_pair_evals=ref,mean_over_reference=evals/ref))
(O/'budget-ratios.json').write_text(json.dumps(diag,indent=2)+'\n')
# Figure from saved empirical curves, via native LaTeX picture primitives only.
# No dependency installation and no experimental engine or statistics bootstrap.
lines=[r'\documentclass{article}',r'\usepackage[paperwidth=7.2in,paperheight=1.65in,margin=0.03in]{geometry}',r'\usepackage{fontspec,graphicx,xcolor}',r'\setmainfont{Times New Roman}',r'\pagestyle{empty}\setlength{\parindent}{0pt}',r'\begin{document}\setlength{\unitlength}{1pt}\begin{picture}(512,112)',r'\put(7,55){\rotatebox{90}{\makebox(0,0){\fontsize{7}{8}\selectfont Share of subsets reaching catalogue}}}']
colors={'harden':'orange!80!black','rigid':'blue!60!black','grow':'green!45!black'}
for i,(key,curves)in enumerate(stats['best_of_k']['curves'].items()):
 x0=30+i*80;y0=23;w=68;h=65
 lines +=[f'\\put({x0},{y0}){{\\line(1,0){{{w}}}}}',f'\\put({x0},{y0}){{\\line(0,1){{{h}}}}}',f'\\put({x0+w/2},{y0+h+10}){{\\makebox(0,0){{\\fontsize{{6}}{{7}}\\selectfont '+key.replace('squ','sq').replace('-in-','/').replace('/n',' $n=')+'$}}']
 for k in stats['best_of_k']['k']:
  x=x0+w*math.log2(k)/5;lines.append(f'\\put({x:.3f},{y0-8}){{\\makebox(0,0){{\\fontsize{{6}}{{7}}\\selectfont {k}}}}}')
 for y in[0,.5,1]:
  if i==0:lines.append(r'\put(%g,%g){\makebox(0,0)[r]{\fontsize{6}{7}\selectfont %g}}'%(x0-6,y0+h*y,y))
 for m,ys in curves.items():
  assert len(ys)==6 and all(0<=y<=1 for y in ys)
  pts=[(x0+w*math.log2(k)/5,y0+h*y)for k,y in zip(stats['best_of_k']['k'],ys)]
  lines.append('{\\color{'+colors[m]+'}')
  for x,y in pts:lines.append(f'\\put({x:.3f},{y:.3f}){{\\rule{{1.4pt}}{{1.4pt}}}}')
  for(x,y),(xx,yy)in zip(pts,pts[1:]):lines.append(f'\\qbezier({x:.3f},{y:.3f})({(x+xx)/2:.3f},{(y+yy)/2:.3f})({xx:.3f},{yy:.3f})')
  lines.append('}')
lines.append(r'\put(250,3){\makebox(0,0){\fontsize{7}{8}\selectfont subset size $k$ (observed pool: 32 runs)}}')
for i,m in enumerate(colors):lines.append(f'\\put({360+i*49},105){{{{\\color{{{colors[m]}}}\\fontsize{{6}}{{7}}\\selectfont {m}}}}}')
lines +=[r'\end{picture}\end{document}']
(J/'figures/bestofk.tex').write_text('\n'.join(lines)+'\n')
(O/'review-analysis-inputs.json').write_text(json.dumps({'source_base':'07e3cbd3c4855e5e19344885fbf672c3d7a0f039','files':[{'path':p,'sha256':h}for p,h in sorted(inputs.items())]},indent=2)+'\n')
print(json.dumps({'tests':len(checks),'inputs':len(inputs),'budgets':diag},indent=2))
