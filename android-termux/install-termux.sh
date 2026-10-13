#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# Run inside Termux from the repository directory.
pkg update -y
pkg install -y git clang make automake autoconf libtool pkg-config openssl libcurl jansson

WORKDIR="$HOME/cpuminer"
if [ ! -d "$WORKDIR/.git" ]; then
  git clone https://github.com/pooler/cpuminer.git "$WORKDIR"
else
  git -C "$WORKDIR" pull --ff-only
fi

cd "$WORKDIR"
./autogen.sh
./configure CFLAGS="-O2"
make -j2

if [ ! -x "$WORKDIR/minerd" ]; then
  echo "Build finished but minerd was not found. Check the build output."
  exit 1
fi

mkdir -p "$PREFIX/bin"
cp "$WORKDIR/minerd" "$PREFIX/bin/digibyte-minerd"
echo "Miner built and installed at: $PREFIX/bin/digibyte-minerd"
echo "Next: run bash android-termux/start-mining.sh from the digi-cpu-miner repository."
