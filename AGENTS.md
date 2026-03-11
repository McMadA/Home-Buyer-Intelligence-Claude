# Knowledge Log

## Recent Insights

- **2026-03-11**: The backend was failing with `400 INVALID_ARGUMENT` from `generativelanguage.googleapis.com` due to an expired Google API key. The issue was traced to `apps/backend/.env` still containing the old key while the root `.env` had the updated key. Ensure all `.env` files in workspaces are in sync when updating credentials.
- **2026-03-11**: The `pnpm dev` command failed to start the backend because `apps/backend` was not included in `pnpm-workspace.yaml` and lacked a `package.json`. It was fixed by creating a minimal `package.json` for the backend with a `dev` script, and adding `apps/backend` to `pnpm-workspace.yaml`.
