import ipaddress
import os
from pathlib import Path

from flask import Flask, abort, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PAGE = "c0-observability.html"
DEFAULT_ALLOWED_CIDRS = (
    "204.14.236.0/24,"
    "66.203.115.0/24,"
    "3.94.34.4/32,"
    "3.95.94.115/32,"
    "34.201.200.177/32,"
    "155.226.242.0/24,"
    "50.112.137.68/32,"
    "52.33.243.73/32,"
    "54.218.242.77/32,"
    "155.226.240.0/24,"
    "155.226.241.0/24,"
    "104.161.246.0/24,"
    "104.161.244.0/24,"
    "104.161.242.0/24,"
    "155.226.244.0/24,"
    "3.0.250.21/32,"
    "3.1.33.218/32,"
    "46.137.240.222/32,"
    "155.226.247.0/24,"
    "155.226.245.0/24,"
    "155.226.246.0/24,"
    "85.222.134.0/24,"
    "155.226.243.0/24,"
    "13.250.175.119/32,"
    "52.220.254.0/32,"
    "54.169.35.174/32"
)

app = Flask(__name__)


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_allowed_networks():
    cidrs = os.getenv("ALLOWED_CIDRS", DEFAULT_ALLOWED_CIDRS)
    networks = []
    for raw_value in cidrs.split(","):
        value = raw_value.strip()
        if not value:
            continue
        networks.append(ipaddress.ip_network(value, strict=False))
    return networks


IP_ALLOWLIST_ENABLED = _env_flag("IP_ALLOWLIST_ENABLED", default=bool(os.getenv("DYNO")))
ALLOWED_NETWORKS = _load_allowed_networks()


def _get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = (request.remote_addr or "").strip()

    if not client_ip:
        return None

    try:
        return ipaddress.ip_address(client_ip)
    except ValueError:
        return None


@app.before_request
def enforce_ip_allowlist():
    if not IP_ALLOWLIST_ENABLED:
        return None

    client_ip = _get_client_ip()
    if client_ip is None:
        abort(403)

    if any(client_ip in network for network in ALLOWED_NETWORKS):
        return None

    abort(403)


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
