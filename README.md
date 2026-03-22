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

Vercel was showing **404** if it auto-detected **Python** (`requirements.txt`) and didn’t emit static files. This repo uses a tiny **`npm run build`** that copies HTML/JS into **`dist/`**, and **`vercel.json`** sets **`outputDirectory`** to `dist`.

1. Push this repo to GitHub (includes `package.json` + `scripts/copy-static.js`).
2. [Vercel](https://vercel.com) → **Add New…** → **Project** → import the repo.
3. **Framework:** Vercel may pick **Other** or **Node** — that’s fine. Root: **`.`**
4. Confirm **Build Command** is `npm run build` and **Output Directory** is `dist` (usually read from `vercel.json`).
5. Deploy. Open the production URL — `/` should serve `index.html`.

If you still see 404: **Project → Settings → General** → clear overrides so `vercel.json` controls build/output, then redeploy.

**API URL:** `api-config.js` sets `window.THE_LEDGER_API_BASE` to your **Render** URL (e.g. `https://the-ledger-nvt1.onrender.com`).  
**Local dev:** when you open `http://localhost:5500`, the app uses **`http://localhost:8000`** for Flask — it does **not** use Render, so you can run `python server.py` locally.

After changing `api-config.js`, commit and push; Vercel redeploys automatically.

## Deploy backend (Flask)

### Render (Web Service)

1. **Root directory:** repo root (or leave default).
2. **Build command:** `pip install -r requirements.txt`
3. **Start command** (this is what the “Required” field wants — **not** `gunicorn your_application.wsgi`; that’s Django):

   ```bash
   gunicorn --bind 0.0.0.0:$PORT server:app
   ```

   - `server` = the file `server.py`
   - `app` = the Flask instance inside it (`app = Flask(__name__)`)

4. Render sets **`PORT`** automatically; `server.py` already reads it if you run `python server.py`, but **Gunicorn** must bind to `$PORT` as above.

**Note:** Free/ephemeral disks may reset `ledger_state.json` on redeploys. For permanent storage, use a Render disk or a database later.

Other hosts (Railway, Fly): same idea — run Gunicorn pointing at `server:app`, or `python server.py` if the platform supports it.

Dependencies: see `requirements.txt` (includes `gunicorn` for Render).

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
