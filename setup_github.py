import urllib.request, json, sys

TOKEN = sys.argv[1]
USER = "sjsilva"
REPO = "dashboard-vendas"

data = json.dumps({
    "name": REPO,
    "description": "Dashboard de Vendas - Streamlit",
    "private": False,
    "auto_init": False
}).encode()

req = urllib.request.Request(
    "https://api.github.com/user/repos",
    data=data,
    headers={
        "Authorization": "token " + TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    },
    method="POST"
)
try:
    resp = urllib.request.urlopen(req)
    r = json.loads(resp.read())
    print("OK:" + r["html_url"])
except urllib.error.HTTPError as e:
    body = json.loads(e.read())
    msg = body.get("message", "")
    if "already exists" in msg or "name already exists" in msg:
        print("OK:https://github.com/" + USER + "/" + REPO)
    else:
        print("ERRO:" + msg)
