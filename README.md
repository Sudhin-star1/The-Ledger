# The Ledger

Static dashboard (`index.html`) + a small **Flask** API under **`backend/`** (`backend/server.py`) that persists shared state to **`backend/ledger_state.json`**.

## Why not “only Vercel”?

- **Vercel** hosts the **frontend** (static `index.html`, `api-config.js`, etc. at the repo root).
- **Flask** runs on **Render** (or Railway/Fly) — not on Vercel’s static hosting.

**Important:** A **`requirements.txt` at the repo root** (and/or a broken **Node build → `dist/`** setup) made Vercel treat the project wrong and show **`500 FUNCTION_INVOCATION_FAILED`**. Python now lives only in **`backend/`**. **`.vercelignore`** excludes `backend/` and other junk from the Vercel upload. The frontend is deployed as **static files** with **no build step**.

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

The frontend is **plain static files** at the repo root (`index.html`, `api-config.js`, etc.). There is **no** `npm run build` — that was removed so Vercel does not run a Node “output” step that can break or look like a serverless app.

1. Push this repo to GitHub.
2. [Vercel](https://vercel.com) → **New Project** → import the repo.
3. **Framework preset:** **Other**.
4. **Root directory:** `.`
5. **Build Command:** leave **empty** (or delete any override).
6. **Output Directory:** leave **empty** (not `dist`).
7. **Install Command:** leave **empty** (no `package.json` in repo).

If you **still** see `FUNCTION_INVOCATION_FAILED` or **500**, open **Project → Settings → General** and **clear** any old **Build / Output / Install** overrides from an earlier setup, then **Redeploy** (or create a **new** project linked to the same repo).

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
