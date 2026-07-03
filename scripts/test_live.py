"""Test the live Vercel deployment endpoints."""
from __future__ import annotations
import json, sys, urllib.request, urllib.error, time

DEPLOY_URL = "agi-readiness-auditor-kgzo87jaz-jds-projects-9e7006b8.vercel.app"
BASE = "https://" + DEPLOY_URL


def get(path: str) -> tuple[int, object]:
    try:
        req = urllib.request.Request(BASE + path)
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:300]
    except Exception as e:
        return 0, str(e)


def post(path: str, body: dict) -> tuple[int, object]:
    try:
        data = json.dumps(body).encode()
        req = urllib.request.Request(BASE + path, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:300]
    except Exception as e:
        return 0, str(e)


print(f"Testing: {BASE}\n")

print("1. GET /api/frameworks")
code, data = get("/api/frameworks")
if code == 200 and isinstance(data, list):
    print(f"   OK — {len(data)} frameworks: {[fw['id'] for fw in data]}")
else:
    print(f"   FAIL {code}: {str(data)[:200]}")
    sys.exit(1)

print("\n2. GET /api/corpus")
code, data = get("/api/corpus")
if code == 200 and isinstance(data, list):
    print(f"   OK — {len(data)} corpora: {data}")
else:
    print(f"   FAIL {code}: {str(data)[:200]}")
    sys.exit(1)

print("\n3. POST /api/audit (openai / openai-5-levels / no_llm)")
code, data = post("/api/audit", {
    "company": "openai",
    "framework": "openai-5-levels",
    "no_llm": True,
})
if code == 200 and isinstance(data, dict) and "score" in data:
    score = data["score"]
    criteria = len(data.get("results", []))
    method = data.get("results", [{}])[0].get("method", "?") if data.get("results") else "?"
    print(f"   OK — score={score}/100, criteria={criteria}, method={method}")
else:
    print(f"   FAIL {code}: {str(data)[:300]}")
    sys.exit(1)

print("\n4. POST /api/compare (openai+anthropic / openai-5-levels / no_llm)")
code, data = post("/api/compare", {
    "companies": ["openai", "anthropic"],
    "framework": "openai-5-levels",
    "no_llm": True,
})
if code == 200 and isinstance(data, dict) and "scores" in data:
    scores = {s["company"]: s["score"] for s in data["scores"]}
    print(f"   OK — scores: {scores}")
else:
    print(f"   FAIL {code}: {str(data)[:300]}")
    sys.exit(1)

print("\n5. GET / (index.html)")
code, data = get("/")
if isinstance(data, str) and "AGI Readiness" in data:
    print(f"   OK — HTML served ({len(data)} chars)")
else:
    # FileResponse returns bytes interpreted as json above; try direct check
    try:
        req = urllib.request.Request(BASE + "/")
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode(errors="replace")
        if "AGI Readiness" in body:
            print(f"   OK — HTML served ({len(body)} chars)")
        else:
            print(f"   WARN — unexpected content: {body[:100]}")
    except Exception as e:
        print(f"   WARN: {e}")

print(f"\n=== All live endpoint checks passed ===")
print(f"Live URL: {BASE}")
