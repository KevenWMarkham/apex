"""Launch the APEX Deploy Wizard end-to-end.

Brings up:
  - Backend  · FastAPI/uvicorn on http://localhost:8000
  - Frontend · Vite/React on http://localhost:5173

Mock mode is the default. Set APEX_FORCE_MOCK=false to call real Azure
(requires `az` CLI + Lab subscription).

Usage:
    python apps/deploy-wizard/launch.py                # default = mock mode
    python apps/deploy-wizard/launch.py --real         # disable APEX_FORCE_MOCK
    python apps/deploy-wizard/launch.py --no-frontend  # backend only
    python apps/deploy-wizard/launch.py --no-backend   # frontend only

The script exits cleanly on Ctrl-C and terminates both child processes.
"""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
API_DIR = APP_ROOT / "api"
WEB_DIR = APP_ROOT / "web"
REPO_ROOT = APP_ROOT.parent.parent

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8000
FRONTEND_PORT = 5173


def _section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def _check_python_deps() -> bool:
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
        import pydantic  # noqa: F401
        return True
    except ImportError as exc:
        print(f"[error] missing Python dep: {exc}")
        print("        Install with:")
        print("        pip install fastapi uvicorn[standard] pydantic httpx pyyaml")
        print(f"        Then install the wizard editable: pip install -e {API_DIR}")
        return False


def _check_node_available() -> bool:
    if shutil.which("npm") is None:
        print("[warn] npm not found; frontend won't start.")
        print(f"       Install Node 20+ then `cd {WEB_DIR} && npm install`.")
        return False
    return True


def _ensure_node_modules() -> bool:
    if (WEB_DIR / "node_modules").exists():
        return True
    print(f"[setup] running `npm install` in {WEB_DIR} (first-run only)...")
    res = subprocess.run(
        ["npm", "install"],
        cwd=WEB_DIR,
        check=False,
    )
    return res.returncode == 0


def _start_backend(mock: bool) -> subprocess.Popen:
    env = os.environ.copy()
    env["APEX_FORCE_MOCK"] = "true" if mock else "false"
    # Ensure apex_wizard is importable.
    sep = ";" if os.name == "nt" else ":"
    env["PYTHONPATH"] = sep.join(filter(None, [
        str(API_DIR / "src"),
        str(REPO_ROOT / "packages" / "apex-core" / "src"),
        str(REPO_ROOT / "apex-m" / "src"),
        env.get("PYTHONPATH", ""),
    ]))
    print(f"[backend] starting uvicorn on http://{BACKEND_HOST}:{BACKEND_PORT}")
    print(f"[backend] APEX_FORCE_MOCK={env['APEX_FORCE_MOCK']}")
    return subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "apex_wizard.main:app",
            "--host", BACKEND_HOST,
            "--port", str(BACKEND_PORT),
            "--reload",
        ],
        cwd=API_DIR,
        env=env,
    )


def _start_frontend() -> subprocess.Popen:
    env = os.environ.copy()
    # Tell Vite where the API is.
    env["VITE_API_URL"] = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
    print(f"[frontend] starting Vite on http://localhost:{FRONTEND_PORT}")
    print(f"[frontend] VITE_API_URL={env['VITE_API_URL']}")
    # Use shell=True on Windows so the npm.cmd extension resolves.
    npm = "npm.cmd" if os.name == "nt" else "npm"
    return subprocess.Popen(
        [npm, "run", "dev", "--", "--port", str(FRONTEND_PORT), "--host"],
        cwd=WEB_DIR,
        env=env,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Launch the APEX Deploy Wizard (backend + frontend).",
    )
    parser.add_argument(
        "--real",
        action="store_true",
        help="Disable APEX_FORCE_MOCK; backend will call real az / Microsoft Graph.",
    )
    parser.add_argument(
        "--no-frontend",
        action="store_true",
        help="Skip the Vite frontend (run backend only).",
    )
    parser.add_argument(
        "--no-backend",
        action="store_true",
        help="Skip the FastAPI backend (run frontend only).",
    )
    args = parser.parse_args()

    if args.no_backend and args.no_frontend:
        print("[error] --no-backend AND --no-frontend leaves nothing to start.")
        return 2

    _section("APEX Deploy Wizard launcher")
    print(f"Repo root: {REPO_ROOT}")
    print(f"API dir:   {API_DIR}")
    print(f"Web dir:   {WEB_DIR}")
    print(f"Mode:      {'real' if args.real else 'mock (APEX_FORCE_MOCK=true)'}")

    procs: list[subprocess.Popen] = []

    try:
        if not args.no_backend:
            if not _check_python_deps():
                return 1
            procs.append(_start_backend(mock=not args.real))
            time.sleep(2.0)  # let uvicorn bind before frontend starts

        if not args.no_frontend:
            if not _check_node_available():
                print("[warn] continuing without frontend")
            else:
                if not _ensure_node_modules():
                    print("[error] npm install failed")
                    raise SystemExit(1)
                procs.append(_start_frontend())

        if not procs:
            print("[error] nothing started")
            return 1

        _section("Ready")
        if not args.no_backend:
            print(f"Backend:  http://{BACKEND_HOST}:{BACKEND_PORT}")
            print(f"  Docs:   http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
            print(f"  Health: http://{BACKEND_HOST}:{BACKEND_PORT}/health")
        if not args.no_frontend:
            print(f"Frontend: http://localhost:{FRONTEND_PORT}/")
            print(f"  Wizard:        http://localhost:{FRONTEND_PORT}/wizard")
            print(f"  Security Gate: http://localhost:{FRONTEND_PORT}/security-gate")
            print(f"  Roadmap:       http://localhost:{FRONTEND_PORT}/roadmap")
            print(f"  Drift:         http://localhost:{FRONTEND_PORT}/drift")
        print("\nPress Ctrl-C to stop both services.\n")

        # Wait until any child exits, then tear the rest down.
        while True:
            for p in procs:
                ret = p.poll()
                if ret is not None:
                    print(f"\n[exit] child pid={p.pid} returned {ret}; stopping siblings...")
                    raise KeyboardInterrupt()
            time.sleep(1.0)

    except KeyboardInterrupt:
        _section("Stopping")
    finally:
        for p in procs:
            try:
                if os.name == "nt":
                    p.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore[attr-defined]
                else:
                    p.terminate()
            except Exception:
                pass
        for p in procs:
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                p.kill()
        print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
