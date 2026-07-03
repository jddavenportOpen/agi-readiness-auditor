"""Check and configure the Vercel project for public access."""
from __future__ import annotations
import json, os, urllib.request, urllib.error
from pathlib import Path

ORG_ID = "team_4hZrv3SL2rmeNVb3ttmIYNa2"
PROJECT_NAME = "agi-readiness-auditor"


def _load_token() -> str:
    p = Path("~/Library/Application Support/com.vercel.cli/auth.json").expanduser()
    with open(p) as f:
        return json.load(f)["token"]


def api(token: str, method: str, path: str, body: dict | None = None) -> dict:
    url = "https://api.vercel.com" + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} → {e.code}: {body_text}") from e


token = _load_token()

# Find the project
print("Looking up project...")
data = api(token, "GET", f"/v9/projects/{PROJECT_NAME}?teamId={ORG_ID}")
project_id = data.get("id", "")
print(f"Project ID: {project_id}")
print(f"Project name: {data.get('name')}")

# Get aliases (production domains)
aliases = data.get("alias", []) or []
print(f"\nAliases/domains:")
for a in aliases:
    print(f"  {a.get('domain')} (type: {a.get('type')})")

# Check protection
protection = data.get("protection", {}) or {}
print(f"\nProtection settings: {json.dumps(protection, indent=2)}")

sso = data.get("ssoProtection") or {}
print(f"SSO protection: {json.dumps(sso, indent=2)}")

# Try to update project to disable Vercel auth for deployments
print("\nAttempting to disable deployment protection...")
try:
    result = api(token, "PATCH", f"/v9/projects/{project_id}?teamId={ORG_ID}", {
        "ssoProtection": None,
    })
    print("Updated project settings.")
except Exception as e:
    print(f"  Could not update: {e}")

# Get the production URL
print("\nGetting latest production deployment URL...")
deps = api(token, "GET", f"/v6/deployments?projectId={project_id}&target=production&teamId={ORG_ID}&limit=3")
for dep in deps.get("deployments", []):
    print(f"  {dep.get('url')} state={dep.get('readyState')} target={dep.get('target')}")
    for alias in dep.get("alias", []):
        print(f"    alias: {alias}")
