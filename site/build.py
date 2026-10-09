"""Assemble the static site into _site/ (deployed by .github/workflows/site.yml; not committed).
    python3 site/build.py
Pages are _head.html + <page>.body.html + _foot.html; data comes from site/data (written by packing.project);
replays and claim folders are copied from the repository so every link resolves."""
import datetime, glob, os, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); OUT = os.path.join(ROOT, '_site')
REPO = os.environ.get('SITE_REPO', 'https://github.com/yoheinakajima/soft-to-rigid')
PAGES = {'index': ('Soft-to-Rigid Packing', 'Hardening disks into polygons as a search to run beside rigid starts: where it finds packings others miss, where it loses, with every run replayable.'),
         'families': ('Families and Replays', 'Every instance, every method, with replays of the best runs.'),
         'journal': ('Research Journal', 'Every campaign in order: question, expectation, rule, result, decision.'),
         'claims': ('Certified Claims', 'Packings below published values, with verifiers.')}
try:
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip()
except Exception:
    commit = 'unknown'
built = datetime.date.today().isoformat()
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
head, foot = open(os.path.join(HERE, '_head.html')).read(), open(os.path.join(HERE, '_foot.html')).read()
for page, (title, desc) in PAGES.items():
    body = open(os.path.join(HERE, page + '.body.html')).read()
    scripts = ''
    if os.path.exists(os.path.join(HERE, page + '.js')):
        scripts = f'<script>\n{open(os.path.join(HERE, page + ".js")).read()}\n</script>'
    if page == 'families':
        scripts = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>\n' + scripts
    html = (head + body + foot).replace('{{TITLE}}', title).replace('{{DESC}}', desc).replace('{{SCRIPTS}}', scripts)
    html = html.replace('{{REPO}}', REPO).replace('{{COMMIT}}', commit).replace('{{BUILT}}', built)
    html = html.replace(f'<a href="{page}.html">', f'<a href="{page}.html" aria-current="page">')
    open(os.path.join(OUT, page + '.html'), 'w').write(html)
shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
shutil.copytree(os.path.join(HERE, 'data'), os.path.join(OUT, 'data'))
for f in glob.glob(os.path.join(ROOT, 'campaigns', '*', 'replays', '**', '*.json'), recursive=True):
    dst = os.path.join(OUT, os.path.relpath(f, ROOT)); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(f, dst)
if os.path.isdir(os.path.join(ROOT, 'claims')):
    shutil.copytree(os.path.join(ROOT, 'claims'), os.path.join(OUT, 'claims'))
pdf = os.path.join(ROOT, 'paper', 'main.pdf')
if os.path.exists(pdf):
    shutil.copy(pdf, os.path.join(OUT, 'paper.pdf'))
abstract = open(os.path.join(ROOT, 'paper', 'sections', 'abstract.tex')).read()
import re as _re
nums = dict(_re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', open(os.path.join(ROOT, 'paper', 'numbers.tex')).read()))
abstract = _re.sub(r'\\(\w+)\{\}', lambda m: nums.get(m.group(1), m.group(0)), abstract).replace('{,}', ',')
body = f'''<header><div class="eyebrow">paper · draft rebuilt with every commit</div><h1>Soft-to-Rigid: Shape Continuation as an Alternative Search for Packing Congruent Shapes</h1>
<p class="lede">{abstract}</p><div class="links"><a href="paper.pdf">PDF</a><a href="{{{{REPO}}}}/tree/main/paper">LaTeX source</a><a href="journal.html">Journal</a></div></header>
<section class="wide"><object data="paper.pdf" type="application/pdf" style="width:100%;height:85vh;border:1px solid var(--rule)"><p><a href="paper.pdf">Download the PDF</a>.</p></object></section>'''
open(os.path.join(OUT, 'paper.html'), 'w').write((head + body + foot).replace('{{TITLE}}', 'Paper').replace('{{DESC}}', 'Soft-to-Rigid: the paper').replace('{{SCRIPTS}}', '')
    .replace('{{REPO}}', REPO).replace('{{COMMIT}}', commit).replace('{{BUILT}}', built).replace('<a href="paper.html">', '<a href="paper.html" aria-current="page">'))
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
print('built', OUT)
