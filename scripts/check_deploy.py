"""Check deployment status and test live endpoints."""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

DEPLOY_ID = "dpl_6jGQA5P81xAnE9w7m8Zj6NtBkGJQ"
DEPLOY_URL = "agi-readiness-auditor-kgzo87jaz-jds-projects-9e7006b8.vercel.app"
ORG_ID = "team_4hZrv3SL2rmeNVb3ttmIYNa2"


def _load_token() -> str:
    p = Path("~/Library/Application Support/com.vercel.cli/auth.json").expanduser()
    with open(p) as f:
        return json.load(f)["token"]


def check_status(token: str) -> str:
    url = f"https://api.vercel.com/v13/deployments/{DEPLOY_ID}?teamId={ORG_ID}"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return data.get("readyState", data.get("status", "?"))


def test_endpoint(url: str) -> tuple[int, str]:
    try:
        req = urllib.request.Request(
            url,
            data=b'{"company":"openai","framework":"openai-5-levels","no_llm":true}',
            method="POST",
        )
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
        return resp.status, body.get("score", "?")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:200]
    except Exception as e:
        return 0, str(e)


token = _load_token()
print("Checking deployment status…")

for attempt in range(12):
    state = check_status(token)
    print(f"  [{attempt+1}] State: {state}")
    if state in ("READY", "ERROR", "CANCELED"):
        break
    time.sleep(15)

if state == "READY":
    print(f"\nDeployment READY: https://{DEPLOY_URL}")
    print("\nTesting /api/frameworks…")
    req = urllib.request.Request(f"https://{DEPLOY_URL}/api/frameworks")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        print(f"  OK — {len(data)} frameworks: {[fw['id'] for fw in data]}")
    except Exception as e:
        print(f"  ERROR: {e}")

    print("\nTesting POST /api/audit (deterministic, openai / openai-5-levels)…")
    code, result = test_endpoint(f"https://{DEPLOY_URL}/api/audit")
    print(f"  HTTP {code}, score={result}")
else:
    print(f"\nDeployment ended in state: {state}")
    print("Check Vercel dashboard for build logs.")
