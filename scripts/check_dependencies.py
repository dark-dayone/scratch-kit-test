#!/usr/bin/env python3
"""Dependency gate: every NEW direct dependency must be approved and must be real.

Run in CI on pull requests:
    python3 scripts/check_dependencies.py --base <base commit sha>

It compares the direct dependency files with the base commit:
    Python   api/requirements.in     (direct packages only; requirements.txt is the pinned output)
    npm      web/package.json        (dependencies and devDependencies)
    Dart     mobile/pubspec.yaml     (dependencies and dev_dependencies)

For every dependency added since the base commit it checks:
    1. FAIL  if it is not listed in docs/approved-dependencies.md (a human approves by adding a row).
    2. FAIL  if it does not exist on its registry (PyPI, npm, pub.dev).
    3. WARN  if it is very new or has only one release (the pattern of a name an attacker registered).
It cannot tell whether an established package is malicious. Standard library only.
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

NEW_DAYS = 30
APPROVED_FILE = "docs/approved-dependencies.md"
FILES = {
    "python": "api/requirements.in",
    "npm": "web/package.json",
    "pub": "mobile/pubspec.yaml",
}


def norm(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirements_in(text):
    names = set()
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or line.startswith("-"):
            continue
        m = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", line)
        if m:
            names.add(norm(m.group(0)))
    return names


def parse_package_json(text):
    if not text.strip():
        return set()
    data = json.loads(text)
    names = set()
    for key in ("dependencies", "devDependencies"):
        names.update(n.lower() for n in data.get(key, {}))
    return names


def parse_pubspec(text):
    names = set()
    lines = text.splitlines()
    in_section = False
    for i, line in enumerate(lines):
        if re.match(r"^(dependencies|dev_dependencies):\s*$", line):
            in_section = True
            continue
        if re.match(r"^[^\s#]", line):
            in_section = False
            continue
        if not in_section:
            continue
        m = re.match(r"^  ([A-Za-z0-9_]+):", line)
        if not m:
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if re.match(r"^    sdk:", nxt):  # flutter, flutter_test: SDK packages
            continue
        names.add(m.group(1).lower())
    return names


PARSERS = {"python": parse_requirements_in, "npm": parse_package_json, "pub": parse_pubspec}


def parse_approved(text):
    approved = set()
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0].lower() in PARSERS:
            name = norm(cells[1]) if cells[0].lower() == "python" else cells[1].lower()
            approved.add((cells[0].lower(), name))
    return approved


def git_show(base, path):
    r = subprocess.run(["git", "show", f"{base}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def read_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dependency-check/1.0"})
    last = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            last = e
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
    raise RuntimeError(f"could not reach registry ({last})")


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def registry_info(eco, name):
    """Return None if the package does not exist, else (first_release_time, release_count)."""
    if eco == "python":
        data = fetch_json(f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json")
        if data is None:
            return None
        times = [parse_time(f["upload_time_iso_8601"]) for files in data["releases"].values() for f in files]
        count = sum(1 for files in data["releases"].values() if files)
        return (min(times) if times else None, count)
    if eco == "npm":
        data = fetch_json("https://registry.npmjs.org/" + urllib.parse.quote(name, safe="@"))
        if data is None:
            return None
        return (parse_time(data["time"]["created"]), len(data.get("versions", {})))
    data = fetch_json(f"https://pub.dev/api/packages/{urllib.parse.quote(name)}")
    if data is None:
        return None
    times = [parse_time(v["published"]) for v in data["versions"] if "published" in v]
    return (min(times) if times else None, len(data["versions"]))


def check(base, lookup=registry_info, show=git_show, read=read_file, now=None):
    now = now or datetime.now(timezone.utc)
    approved = parse_approved(read(APPROVED_FILE))
    errors, warnings = [], []
    for eco, path in FILES.items():
        parse = PARSERS[eco]
        added = parse(read(path)) - parse(show(base, path))
        for name in sorted(added):
            if (eco, name) not in approved:
                errors.append(f"{eco} package '{name}' was added in {path} but is not in {APPROVED_FILE}. "
                              f"A human must approve it (add a row) after the plan review.")
            info = lookup(eco, name)
            if info is None:
                errors.append(f"{eco} package '{name}' does not exist on its registry. "
                              f"It may be an invented or misspelled name.")
                continue
            first, count = info
            if first is not None and (now - first).days < NEW_DAYS:
                warnings.append(f"{eco} package '{name}' was first published only {(now - first).days} days ago.")
            if count <= 1:
                warnings.append(f"{eco} package '{name}' has only {count} release(s).")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="base commit to compare against")
    args = ap.parse_args()
    try:
        errors, warnings = check(args.base)
    except RuntimeError as e:
        print(f"::error::Dependency check failed: {e}. Re-run the job.")
        return 1
    for w in warnings:
        print(f"::warning::{w}")
    for e in errors:
        print(f"::error::{e}")
    if not errors:
        print("Dependency check passed." + (" See warnings above." if warnings else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
