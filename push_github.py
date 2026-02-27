import subprocess, sys, os

TOKEN = sys.argv[1]
USER = "claudioluizsap-lab"
REPO = "dashboard-vendas"
PROJ = r"D:\Users\Claudio\Documents\verdent-projects\new-project"
GIT = r"C:\Program Files\Git\bin\git.exe"

def run(cmd, **kw):
    r = subprocess.run(cmd, cwd=PROJ, capture_output=True, text=True, **kw)
    out = (r.stdout + r.stderr).strip()
    if out: print(out)
    return r.returncode

run([GIT, "init"])
run([GIT, "config", "user.email", "dashboard@vendas.com"])
run([GIT, "config", "user.name", "Claudio"])
run([GIT, "add", "app.py", "requirements.txt", ".gitignore", "vendas.xlsx"])
run([GIT, "commit", "-m", "Dashboard de Vendas v3.0"])
run([GIT, "branch", "-M", "main"])
run([GIT, "remote", "remove", "origin"])
run([GIT, "remote", "add", "origin", f"https://{USER}:{TOKEN}@github.com/{USER}/{REPO}.git"])
rc = run([GIT, "push", "-u", "origin", "main"])
if rc == 0:
    print(f"\nPUSH OK! https://github.com/{USER}/{REPO}")
else:
    print("\nErro no push")
