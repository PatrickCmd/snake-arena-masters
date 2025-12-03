#!/usr/bin/env bash
set -euo pipefail

echo "========== FRONTEND BUILD START =========="

# Install dependencies
echo "[INFO] Installing dependencies..."
npm ci

# Build production bundle
echo "[INFO] Building production bundle..."
npm run build

echo "[INFO] Build output:"
ls -lh dist/

echo "[INFO] Frontend build complete!"
echo "========== FRONTEND BUILD END =========="
