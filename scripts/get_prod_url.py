"""Get the stable production URL for this Vercel project."""
import json, urllib.request, urllib.error
from pathlib import Path

ORG_ID = "team_4hZrv3SL2rmeNVb3ttmIYNa2"
PROJECT_ID = "prj_vR0rucd5b3maRGt7MQKO374aheSE"
DEPLOY_ID = "dpl_6jGQA5P81xAnE9w7m8Zj6NtBkGJQ"


def _load_token() -> str:
    p = Path("~/Library/Application Support/com.vercel.cli/auth.json").expanduser()
    with open(p) as f:
        return json.load(f)["token"]


def api(token: str, path: str) -> dict:
    url = "https://api.vercel.com" + path
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors="replace")}


token = _load_token()

# Get deployment aliases
dep = api(token, f"/v13/deployments/{DEPLOY_ID}?teamId={ORG_ID}")
print("Deployment aliases:")
for a in dep.get("alias", []):
    print(f"  {a}")

print("\nDeployment URL:", dep.get("url"))
print("Deployment inspectorUrl:", dep.get("inspectorUrl"))

# Get project aliases
proj = api(token, f"/v9/projects/{PROJECT_ID}?teamId={ORG_ID}")
print("\nProject aliases:")
for a in proj.get("alias", []):
    print(f"  {a.get('domain')} type={a.get('type')}")
print("Project link:", proj.get("link", {}).get("repoId", "no repo linked"))
