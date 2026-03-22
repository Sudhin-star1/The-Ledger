# The Ledger

Static dashboard (`index.html`) + a small **Flask** API under **`backend/`** (`backend/server.py`) that persists shared state to **`backend/ledger_state.json`**.

## Why not “only Vercel”?

- **Vercel** hosts the **frontend** (HTML/CSS/JS built into `dist/`).
- **Flask** runs on **Render** (or Railway/Fly) — not on Vercel’s static hosting.

**Important:** A **`requirements.txt` at the repo root** made Vercel treat the project as **Python** and try to run **serverless functions**, which caused **`500 FUNCTION_INVOCATION_FAILED`**. Python now lives only in **`backend/`**, and **`.vercelignore`** excludes that folder from the Vercel deployment.

**Recommended split**

1. Deploy **this repo** to **Vercel** (static output from `npm run build` → `dist/`).
2. Deploy **`backend/`** to **Render** (or similar).
3. Set the API URL in **`api-config.js`** (`window.THE_LEDGER_API_BASE`).

## Local dev

- **Frontend:** from repo root, e.g. `python3 -m http.server 5500` and open `http://localhost:5500`.
- **API:** from repo root:

  ```bash
  cd backend && python3 server.py
  ```

  Flask listens on **`http://localhost:8000`**. The UI uses that when hostname is `localhost` / `127.0.0.1`.

## Deploy frontend on Vercel

1. Push this repo to GitHub (`package.json`, `scripts/copy-static.js`, `vercel.json`).
2. [Vercel](https://vercel.com) → **New Project** → import the repo.
3. **Root directory:** `.`  
4. **Build Command:** `npm run build` · **Output Directory:** `dist` (from `vercel.json`).
5. **Framework:** Other / Node is fine — there must be **no** root `requirements.txt` (Python is under `backend/` only).

If you still see errors: **Settings → General** → remove overrides for build/output, then **Redeploy**.

**Production API URL** is set in **`api-config.js`** (e.g. your Render URL).

## Deploy backend on Render

1. **Root Directory:** `backend` (not the monorepo root).
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:**

   ```bash
   gunicorn --bind 0.0.0.0:$PORT server:app
   ```

4. Data file: **`backend/ledger_state.json`** (gitignored). Free tier disks may reset on redeploys.

### Migrating an existing Render service

If the service was created with **root** as the app directory, change **Root Directory** to **`backend`**, save, and redeploy. Copy any existing **`ledger_state.json`** into **`backend/`** on the host if needed.

## Git: push

```bash
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

## Privacy

`ledger_state.json` is gitignored (anywhere in the repo) so your data is not committed by mistake.
