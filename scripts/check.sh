#!/usr/bin/env bash
# Local check set: the same tools CI runs, so failures are caught before a push.
# Run after every slice. Results are developer feedback only; they never replace
# the "CI gate" check on GitHub.
# Needs the dev tools installed (api/requirements-dev.txt, Node, Flutter) and,
# for the secret scan, the gitleaks CLI. A missing tool FAILS the script on purpose.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
run() { echo; echo "== $*"; "$@" || { echo "FAILED: $*"; fail=1; }; }

if command -v gitleaks >/dev/null 2>&1; then
  run gitleaks git --redact --no-banner
else
  echo "FAILED: gitleaks is not installed (secret scan not run)"; fail=1
fi

if [ -f api/requirements.txt ]; then
  pushd api >/dev/null
  run ruff check .
  run ruff format --check .
  run mypy .
  run bandit -r . -ll --exclude ./tests,./.venv,./venv
  run pip-audit -r requirements.txt
  run pytest
  popd >/dev/null
fi
if [ -f web/package.json ]; then
  pushd web >/dev/null
  run npm run lint
  run npm run typecheck
  run npm test
  run npm run build
  popd >/dev/null
fi
if [ -f mobile/pubspec.yaml ]; then
  pushd mobile >/dev/null
  run dart format --output=none --set-exit-if-changed .
  run flutter analyze
  run flutter test
  popd >/dev/null
fi

echo
if [ "$fail" -eq 0 ]; then echo "All local checks passed."; else echo "Some local checks FAILED."; fi
exit "$fail"
