#!/usr/bin/env bash
# Simulated staging deploy for the lab — prints success without touching a real server.
set -euo pipefail

VERSION="${1:-0.1.0}"
DIST_DIR="dist"

if [ ! -d "$DIST_DIR" ] || [ -z "$(ls -A "$DIST_DIR" 2>/dev/null)" ]; then
  echo "ERROR: dist/ is empty. Run 'uv build' first."
  exit 1
fi

echo "Deploying invoice-utils v${VERSION} to staging..."
echo "  Artifacts: $(ls "$DIST_DIR" | tr '\n' ' ')"
echo "  Health check: OK"
echo "  URL: https://staging.example.com/invoice-utils/${VERSION}"
echo "DEPLOY_SUCCESS"
