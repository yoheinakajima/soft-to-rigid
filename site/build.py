"""Assemble the static site into _site/ (deployed by .github/workflows/site.yml; not committed).
    python3 site/build.py
Pages are _head.html + <page>.body.html + _foot.html; data comes from site/data (written by packing.project);
replays and claim folders are copied from the repository so every link resolves."""
import datetime, glob, os, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); OUT = os.path.join(ROOT, '_site')
REPO = os.environ.get('SITE_REPO', 'https://github.com/yoheinakajima/soft-to-rigid')
PAGES = {'index': ('Soft-to-Rigid Packing', 'Does the path a piece takes through shape space change which packings a search finds? An equal-budget study across 2D and 3D families, with every run replayable.'),
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
for extra in ('paper.html', 'paper.pdf'):
    src = os.path.join(ROOT, 'paper', 'build', extra)
    if os.path.exists(src): shutil.copy(src, os.path.join(OUT, extra))
if not os.path.exists(os.path.join(OUT, 'paper.html')):
    open(os.path.join(OUT, 'paper.html'), 'w').write((head + '<header><h1>Paper</h1><p class="lede">The paper is being written. Its outline is in <a href="{{REPO}}/blob/main/paper/OUTLINE.md">paper/OUTLINE.md</a>.</p></header>' + foot)
        .replace('{{TITLE}}', 'Paper').replace('{{DESC}}', 'The paper').replace('{{SCRIPTS}}', '').replace('{{REPO}}', REPO).replace('{{COMMIT}}', commit).replace('{{BUILT}}', built))
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
print('built', OUT)
