#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
PIDFILE="$HOME/.digibyte-miner.pid"

if [ ! -f "$PIDFILE" ]; then
  echo "No PID file found; miner may already be stopped."
  exit 0
fi

PID="$(cat "$PIDFILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  for _ in 1 2 3 4 5; do
    sleep 1
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
  done
  if kill -0 "$PID" 2>/dev/null; then
    echo "Miner did not stop cleanly. Try: kill $PID"
    exit 1
  fi
fi
rm -f "$PIDFILE"
echo "DigiByte miner stopped."
