#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
PIDFILE="$HOME/.digibyte-miner.pid"
LOGFILE="$HOME/digibyte-miner.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "RUNNING (PID $(cat "$PIDFILE"))"
else
  echo "STOPPED"
fi

if [ -f "$LOGFILE" ]; then
  echo "Recent miner output:"
  tail -n 20 "$LOGFILE"
fi
