#!/bin/bash
set -euo pipefail

echo "========== ENTRYPOINT START =========="

# Show Python + environment
echo "[INFO] Python path:"
ls -l /app/.venv/bin/ || true

echo "[INFO] Alembic file info:"
if [ -f /app/.venv/bin/alembic ]; then
    file /app/.venv/bin/alembic || true
else
    echo "[ERROR] Alembic binary not found in venv!"
fi

echo "[INFO] Python binary info:"
file /app/.venv/bin/python || true

echo "[INFO] Alembic shebang:"
head -n 1 /app/.venv/bin/alembic || true

echo "[INFO] Checking shared libraries used by Alembic python:"
ldd /app/.venv/bin/python || true

echo "========== DATABASE WAIT CHECK =========="

if [ -z "${DATABASE_URL:-}" ]; then
  echo "[WARN] No DATABASE_URL provided. Skipping DB wait."
else
  DB_HOST=$(echo "$DATABASE_URL" | sed -E 's/.*@([^:/]+).*/\1/')
  DB_PORT=$(echo "$DATABASE_URL" | sed -E 's/.*:([0-9]+)\/.*/\1/')

  echo "[INFO] Parsed DB host: $DB_HOST"
  echo "[INFO] Parsed DB port: $DB_PORT"

  MAX_RETRIES=20
  RETRY_DELAY=2

  for i in $(seq 1 $MAX_RETRIES); do
    echo "[INFO] Checking DB availability... attempt $i/$MAX_RETRIES"
    if pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then
        echo "[INFO] Database is ready!"
        break
    fi
    sleep $RETRY_DELAY
  done
fi

echo "========== RUNNING ALEMBIC =========="

if ! /app/.venv/bin/python -m alembic upgrade head; then
    echo "[ERROR] Alembic migration failed."
    exit 1
fi

echo "========== STARTING UVICORN =========="
exec /app/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
