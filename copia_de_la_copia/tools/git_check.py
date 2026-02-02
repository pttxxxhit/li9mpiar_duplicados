import subprocess, os, sys
repo = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print('repo:', repo)
for cmd in [['git','rev-parse','--is-inside-work-tree'], ['git','status','--porcelain','-b'], ['git','add','main_minimal.py','BOTONES.md'], ['git','commit','-m','Clean main_minimal: remove preview, add diagnostics buttons; add BOTONES.md explaining buttons'], ['git','rev-parse','--abbrev-ref','HEAD'], ['git','log','-n','5','--oneline']]:
    try:
        print('\n$', ' '.join(cmd))
        out = subprocess.check_output(cmd, cwd=repo, stderr=subprocess.STDOUT, text=True)
        print(out)
    except subprocess.CalledProcessError as e:
        print('ERROR (rc=%s):' % e.returncode)
        print(e.output)
        # continue
print('\nDone')
