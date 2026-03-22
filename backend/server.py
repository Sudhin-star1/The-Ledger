from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Manual CORS headers (so the frontend can call this API across domains)
@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "ledger_state.json")

DEFAULT_STATE = {
    "logs": [],
    "domainHours": {},
    "currentStreak": 0,
    "bestStreak": 0,
    "tombstoneExcuses": [],
    "missedDays": 0,
    "totalPenalty": 0,
    "lastProcessedDate": None,
}


def load_state():
    """Load ledger state from disk or return default."""
    if not os.path.exists(DATA_FILE):
        return DEFAULT_STATE.copy()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ensure we always have all expected keys
        state = DEFAULT_STATE.copy()
        state.update(data)
        return state
    except Exception:
        # on any error, fall back to a clean default state
        return DEFAULT_STATE.copy()


def save_state(data: dict) -> None:
    """Persist ledger state to disk."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


@app.get("/")
def root():
    """Render health check + browser hint (UI is on Vercel; this service is API-only)."""
    return jsonify(
        {
            "service": "The Ledger API",
            "ok": True,
            "endpoints": {"GET /state": "load ledger", "POST /state": "save ledger"},
            "note": "Open your Vercel site for the dashboard; this URL is only the backend.",
        }
    )


@app.get("/state")
def get_state():
    """Return the current ledger state."""
    return jsonify(load_state())


@app.post("/state")
def post_state():
    """Replace the current ledger state with the provided one."""
    data = request.get_json(force=True) or {}
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "state must be a JSON object"}), 400

    # Merge over defaults to avoid missing keys
    incoming = DEFAULT_STATE.copy()
    incoming.update(data)

    # Safety: don't overwrite a richer backend state with an empty/partial payload.
    current = load_state()
    try:
        current_logs = current.get("logs", [])
        incoming_logs = incoming.get("logs", [])
        if (
            isinstance(current_logs, list)
            and isinstance(incoming_logs, list)
            and len(incoming_logs) < len(current_logs)
        ):
            return jsonify({"ok": True, "ignored": True, "reason": "incoming has fewer logs than backend"})
    except Exception:
        pass

    save_state(incoming)
    return jsonify({"ok": True, "ignored": False})


@app.route("/state", methods=["OPTIONS"])
def options_state():
    # Handle CORS preflight for POST with JSON
    resp = jsonify({})
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    # Railway/Render/etc. often set PORT; local dev defaults to 8000
    port = int(os.environ.get("PORT", "8000"))
    # Local: set FLASK_DEBUG=1 for auto-reload; production should leave unset
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
