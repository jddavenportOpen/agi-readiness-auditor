"""Deploy the agi-readiness-auditor project to Vercel via the REST API.

Run from the project root:
  python3 scripts/vercel_deploy.py [--prod]

Uses the Vercel token already stored in:
  ~/Library/Application Support/com.vercel.cli/auth.json
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORG_ID = "team_4hZrv3SL2rmeNVb3ttmIYNa2"
PROJECT_NAME = "agi-readiness-auditor"

INCLUDE_GLOBS = [
    "index.html",
    "requirements.txt",
    "vercel.json",
    "Procfile",
    "railway.toml",
    "README.md",
    "WORKPLAN.md",
    "api/__init__.py",
    "api/app.py",
    "agi_auditor/__init__.py",
    "agi_auditor/__main__.py",
    "agi_auditor/analyzer.py",
    "agi_auditor/corpus.py",
    "agi_auditor/frameworks.py",
    "agi_auditor/report.py",
    "agi_auditor/corpus/*.json",
    "agi_auditor/frameworks/*.json",
]

EXCLUDE_PATTERNS = {".git", "__pycache__", ".pyc", ".pytest_cache"}


def _load_token() -> str:
    paths = [
        Path("~/Library/Application Support/com.vercel.cli/auth.json").expanduser(),
        Path("~/.vercel/auth.json").expanduser(),
        Path("~/.config/vercel/auth.json").expanduser(),
    ]
    for p in paths:
        if p.exists():
            with open(p) as f:
                return json.load(f)["token"]
    tok = os.environ.get("VERCEL_TOKEN", "")
    if tok:
        return tok
    raise RuntimeError("No Vercel auth token found. Run `vercel login` or set VERCEL_TOKEN.")


def _collect_files() -> list[Path]:
    files: list[Path] = []
    for pattern in INCLUDE_GLOBS:
        files.extend(PROJECT_ROOT.glob(pattern))
    seen: set[str] = set()
    out: list[Path] = []
    for f in files:
        if not f.is_file():
            continue
        key = str(f)
        if key in seen:
            continue
        if any(ex in f.parts or ex in f.name for ex in EXCLUDE_PATTERNS):
            continue
        seen.add(key)
        out.append(f)
    return sorted(out)


def _file_sha1(content: bytes) -> str:
    return hashlib.sha1(content).hexdigest()


def _api(token: str, method: str, path: str, body: dict | None = None) -> dict:
    url = "https://api.vercel.com" + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"Vercel API {method} {path} → {e.code}: {body_text}") from e


def _upload_file(token: str, content: bytes) -> str:
    digest = _file_sha1(content)
    url = "https://api.vercel.com/v2/files"
    req = urllib.request.Request(url, data=content, method="POST")
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/octet-stream")
    req.add_header("x-vercel-digest", digest)
    req.add_header("x-vercel-size", str(len(content)))
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pass
    except urllib.error.HTTPError as e:
        if e.code == 409:
            pass  # file already uploaded — that's fine
        else:
            body_text = e.read().decode(errors="replace")
            raise RuntimeError(f"File upload error {e.code}: {body_text}") from e
    return digest


def deploy(prod: bool = False) -> str:
    token = _load_token()
    print("Loaded Vercel token.")

    # Verify auth
    user_data = _api(token, "GET", "/v2/user")
    username = user_data.get("user", {}).get("username", "?")
    print(f"Authenticated as: {username}")

    files = _collect_files()
    print(f"Uploading {len(files)} files…")

    deployment_files = []
    for fpath in files:
        content = fpath.read_bytes()
        digest = _upload_file(token, content)
        rel = str(fpath.relative_to(PROJECT_ROOT))
        deployment_files.append({"file": rel, "sha": digest, "size": len(content)})
        print(f"  {rel} ({len(content)} bytes)")

    # Build deployment payload
    target = "production" if prod else "preview"
    payload: dict = {
        "name": PROJECT_NAME,
        "files": deployment_files,
        "projectSettings": {
            "framework": None,
            "installCommand": "pip install -r requirements.txt",
            "buildCommand": None,
            "outputDirectory": None,
        },
        "target": target,
    }

    print(f"\nCreating {target} deployment…")
    result = _api(token, "POST", "/v13/deployments?teamId=" + ORG_ID, payload)
    deploy_url = result.get("url", "")
    deploy_id = result.get("id", "")
    state = result.get("readyState", result.get("status", "?"))
    print(f"Deployment created: {deploy_id}")
    print(f"URL: https://{deploy_url}")
    print(f"State: {state}")
    return deploy_url


if __name__ == "__main__":
    prod = "--prod" in sys.argv
    try:
        url = deploy(prod=prod)
        print("\nDone:", "https://" + url)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)
