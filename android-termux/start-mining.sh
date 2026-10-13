#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MINER="${PREFIX:-/data/data/com.termux/files/usr}/bin/digibyte-minerd"
PIDFILE="$HOME/.digibyte-miner.pid"
LOGFILE="$HOME/digibyte-miner.log"
ADDRESS="DPDCmF5RUXoPCyaTHunvHgpc9ZsQj55Bjt"
POOL="stratum+tcp://digi.hmpool.io:3337"
THREADS="${DIGIBYTE_THREADS:-2}"

if [ ! -x "$MINER" ]; then
  echo "Miner not installed. First run: bash android-termux/install-termux.sh"
  exit 1
fi

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "DigiByte miner is already running (PID $(cat "$PIDFILE"))."
  exit 0
fi

# Keep CPU use modest by default; lower DIGIBYTE_THREADS to 1 if the phone heats up.
nohup "$MINER" -a sha256d -o "$POOL" -u "${ADDRESS}.android" -p x -t "$THREADS" >"$LOGFILE" 2>&1 &
echo $! > "$PIDFILE"
sleep 2
if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "Miner started (PID $(cat "$PIDFILE"))."
  echo "Log: $LOGFILE"
  echo "Stop with: bash android-termux/stop-mining.sh"
else
  rm -f "$PIDFILE"
  echo "Miner did not stay running. Check log: $LOGFILE"
  tail -n 40 "$LOGFILE" || true
  exit 1
fi
