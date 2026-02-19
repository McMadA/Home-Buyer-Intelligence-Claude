#!/bin/bash
# Generate TypeScript types from FastAPI OpenAPI spec
set -e

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
OUTPUT_DIR="libs/shared-types/src"

echo "Fetching OpenAPI spec from $BACKEND_URL..."
curl -s "$BACKEND_URL/openapi.json" -o /tmp/openapi.json

echo "Generating TypeScript types..."
mkdir -p "$OUTPUT_DIR"
npx openapi-typescript /tmp/openapi.json -o "$OUTPUT_DIR/index.ts"

echo "Done! Types written to $OUTPUT_DIR/index.ts"
