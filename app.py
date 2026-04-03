from pathlib import Path

from flask import Flask, abort, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PAGE = "c0-observability.html"

app = Flask(__name__)


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, DEFAULT_PAGE)


@app.get("/<path:filename>")
def serve_project_file(filename: str):
    file_path = BASE_DIR / filename
    if not file_path.is_file():
        abort(404)
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
