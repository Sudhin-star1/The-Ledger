# The Ledger

Static dashboard (`index.html`) + a small **Flask** API (`server.py`) that persists shared state to `ledger_state.json`.

## Why not “only Vercel”?

- **Vercel** is great for the **frontend** (HTML/CSS/JS).
- **`server.py` is not a good fit for plain Vercel static hosting**: it needs a long‑running process and a writable file (or a database). Vercel serverless can be adapted, but this repo uses the simple Flask + JSON file approach.

**Recommended split**

1. Deploy **this repo’s static files** to **Vercel** (root `index.html`).
2. Deploy **`server.py`** to **Railway**, **Render**, **Fly.io**, or any VPS.
3. Set the backend URL in **`api-config.js`** (`window.THE_LEDGER_API_BASE`).

Local dev: run Flask on port `8000` and serve the folder with any static server (e.g. `python -m http.server 5500`).

## Deploy frontend on Vercel

1. Push this repo to GitHub (see below).
2. In Vercel: **New Project** → import the repo → Framework: **Other** (static).
3. After deploy, open your Vercel URL — you should see `index.html`.
4. Edit **`api-config.js`** in the repo to set `window.THE_LEDGER_API_BASE` to your deployed Flask URL, commit, and redeploy.

## Deploy backend (Flask)

Example (Railway / Render — adjust for your provider):

- Start command: `python server.py` (or `gunicorn` in production).
- Set `PORT` if the platform injects it (you may need a one-line change to read `os.environ.get("PORT", "8000")` — add if your host requires it).
- Ensure the filesystem path for `ledger_state.json` is persistent on that platform (ephemeral disks reset on some free tiers).

Dependencies: see `requirements.txt`.

## Git: create repo and push

From this folder:

```bash
cd "/path/to/The Ledger"
git init
git add .
git commit -m "Initial commit: The Ledger"
```

Create an empty repository on GitHub (no README/license if you already have files), then:

```bash
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Privacy

`ledger_state.json` is listed in `.gitignore` so your personal ledger is not committed by mistake.
