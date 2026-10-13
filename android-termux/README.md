# DigiByte CPU miner on Android (Termux)

These scripts are an **experimental community setup**, not a guaranteed Android build. The upstream cpuminer project may fail to compile or connect on some Android/Termux versions. This repository does not run mining in GitHub Actions.

## Requirements
- Android device you own or have permission to use.
- Termux installed from its official F-Droid or GitHub distribution (avoid obsolete Play Store builds).
- Internet connection. Mining on a phone can generate substantial heat, drain the battery, and be unprofitable. Do not mine while charging unattended; stop if the phone becomes hot.

## Setup
1. Open Termux and install Git: `pkg install git`.
2. Clone this repository: `git clone https://github.com/willamesraphaeldamoto-creator/digi-cpu-miner.git`
3. Enter the directory: `cd digi-cpu-miner`
4. Build the miner: `bash android-termux/install-termux.sh`
5. Start: `bash android-termux/start-mining.sh`
6. Check status/logs: `bash android-termux/status-mining.sh`
7. Stop: `bash android-termux/stop-mining.sh`

Default worker is `DPDCmF5RUXoPCyaTHunvHgpc9ZsQj55Bjt.android`, pool `stratum+tcp://digi.hmpool.io:3337`, algorithm `sha256d`, and two CPU threads. Reduce load to one thread with `DIGIBYTE_THREADS=1 bash android-termux/start-mining.sh`.

## Notes
- `miner.yml` is a configuration reference; cpuminer does not automatically read that YAML file. The start script passes its settings as command-line arguments.
- Keep Termux open or use Android's battery/background settings as needed; Android may suspend background processes. These scripts do not guarantee continuous 24/7 mining.
- The pool endpoint and algorithm are user-supplied and have not been independently tested here. Confirm the pool's current instructions and payout requirements.
- This is CPU mining, not a promise of earnings. DigiByte difficulty and phone performance may make rewards negligible.
