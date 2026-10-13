#!/usr/bin/env python3
"""
DigiByte Termux controller.
This Python script controls an external cpuminer executable; it does not mine by itself.
"""
import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

POOL = "stratum+tcp://digi.hmpool.io:3337"
WALLET = "DPDCmF5RUXoPCyaTHunvHgpc9ZsQj55Bjt"
WORKER = "android"
PID_FILE = Path.home() / ".digibyte-miner.pid"
LOG_FILE = Path.home() / "digibyte-miner.log"


def miner_path():
    configured = os.environ.get("DIGIBYTE_MINER")
    candidates = [configured, shutil.which("digibyte-minerd"), shutil.which("minerd")]
    for item in candidates:
        if item and Path(item).is_file() and os.access(item, os.X_OK):
            return item
    return None


def read_pid():
    try:
        return int(PID_FILE.read_text().strip())
    except (OSError, ValueError):
        return None


def running(pid):
    if not pid or pid <= 1:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def status():
    pid = read_pid()
    if running(pid):
        print(f"Status: RUNNING (PID {pid})")
    else:
        print("Status: STOPPED")
    print(f"Pool: {POOL}")
    print(f"Worker: {WALLET}.{WORKER}")
    print(f"Log: {LOG_FILE}")
    if LOG_FILE.exists():
        print("\n--- últimas linhas do log ---")
        try:
            lines = LOG_FILE.read_text(errors="replace").splitlines()
            print("\n".join(lines[-12:]))
        except OSError as exc:
            print(f"Não foi possível ler o log: {exc}")


def start(threads):
    pid = read_pid()
    if running(pid):
        print(f"Minerador já está ativo (PID {pid}).")
        return 0
    binary = miner_path()
    if not binary:
        print("ERRO: não encontrei o minerador cpuminer.")
        print("Instale/compile um minerador compatível e disponibilize 'digibyte-minerd' no PATH.")
        print("Este Python é um controlador; ele não implementa mineração por conta própria.")
        return 2
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("ab") as log:
        try:
            proc = subprocess.Popen(
                [binary, "-a", "sha256d", "-o", POOL,
                 "-u", f"{WALLET}.{WORKER}", "-p", "x", "-t", str(threads)],
                stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        except OSError as exc:
            print(f"Falha ao iniciar minerador: {exc}")
            return 3
    time.sleep(2)
    if proc.poll() is not None:
        print("O minerador encerrou logo após iniciar. Veja o log:")
        print(LOG_FILE)
        return 4
    PID_FILE.write_text(str(proc.pid))
    print(f"Minerador iniciado (PID {proc.pid}).")
    print(f"Pool: {POOL}")
    print(f"Log: {LOG_FILE}")
    print("Use 'python digibyte.py status' para acompanhar e 'python digibyte.py stop' para parar.")
    print("Monitore a temperatura; pare se o telefone aquecer.")
    return 0


def stop():
    pid = read_pid()
    if not running(pid):
        PID_FILE.unlink(missing_ok=True)
        print("Minerador já está parado.")
        return 0
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        PID_FILE.unlink(missing_ok=True)
        print("Minerador já estava parado.")
        return 0
    for _ in range(10):
        time.sleep(1)
        if not running(pid):
            PID_FILE.unlink(missing_ok=True)
            print("Minerador parado.")
            return 0
    print(f"O processo {pid} ainda está ativo; tente 'kill {pid}' no Termux.")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Controlador de mineração DigiByte para Termux")
    sub = parser.add_subparsers(dest="command", required=True)
    p_start = sub.add_parser("start", help="iniciar mineração")
    p_start.add_argument("--threads", type=int, default=2, help="threads de CPU (padrão: 2)")
    sub.add_parser("stop", help="parar mineração")
    sub.add_parser("status", help="ver estado e log")
    args = parser.parse_args()
    if args.command == "start":
        if args.threads < 1 or args.threads > 16:
            parser.error("--threads deve estar entre 1 e 16")
        return start(args.threads)
    if args.command == "stop":
        return stop()
    status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
