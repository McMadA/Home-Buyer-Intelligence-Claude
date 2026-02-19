#!/bin/bash
# Run Alembic database migrations
set -e

cd apps/backend

echo "Running database migrations..."
uv run alembic upgrade head

echo "Migrations complete!"
