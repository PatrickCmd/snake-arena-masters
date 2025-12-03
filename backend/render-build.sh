#!/usr/bin/env bash
set -euo pipefail

echo "========== RENDER BUILD START =========="

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "[INFO] Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "[INFO] uv version: $(uv --version)"

# Install dependencies
echo "[INFO] Installing dependencies..."
uv sync --frozen

# Run database migrations
echo "[INFO] Running database migrations..."
uv run alembic upgrade head

echo "[INFO] Build complete!"
echo "========== RENDER BUILD END =========="
