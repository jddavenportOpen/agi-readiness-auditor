"""Quick smoke test against the canonical production URL."""
import json, urllib.request, urllib.error, sys

BASE = "https://agi-readiness-auditor.vercel.app"

def post(path: str, body: dict) -> tuple[int, object]:
    try:
        data = json.dumps(body).encode()
        req = urllib.request.Request(BASE + path, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:200]
    except Exception as e:
        return 0, str(e)

print(f"Testing canonical URL: {BASE}")

req = urllib.request.Request(BASE + "/api/frameworks")
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    print(f"GET /api/frameworks -> OK ({len(data)} frameworks)")
except Exception as e:
    print(f"GET /api/frameworks -> ERROR: {e}")
    sys.exit(1)

code, result = post("/api/audit", {
    "company": "anthropic", "framework": "anthropic-rsp", "no_llm": True
})
if code == 200:
    print(f"POST /api/audit -> OK score={result['score']}/100")
else:
    print(f"POST /api/audit -> FAIL {code}: {result}")
    sys.exit(1)

print(f"\nProduction URL verified: {BASE}")
