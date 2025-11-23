#!/bin/bash
set -e

INSTANCE="$1"

if [ -z "$INSTANCE" ]; then
  echo "Usage: SESSION=xxx bash install-rezee.sh <instance>"
  exit 1
fi

echo "[+] Buat folder instance..."
mkdir -p /root/ubot/$INSTANCE
cd /root/ubot/$INSTANCE

echo "[+] Tulis ENV..."
cat > .env <<EOF
SESSION="${SESSION}"
OWNER_ID="${OWNER_ID}"
LOG_CHANNEL="${LOG_CHANNEL}"
EOF

echo "[+] Download file Rezee Ubot..."
curl -s https://raw.githubusercontent.com/USERNAME/REPO/main/rezee.py -o rezee.py

echo "[+] Install Telethon..."
pip install telethon --quiet || pip3 install telethon --quiet

echo "[+] Jalankan screen..."
screen -dmS "ubot-$INSTANCE" bash -c '
  export $(grep -v "^#" .env | xargs)
  while true; do
    python3 rezee.py
    sleep 3
  done
'

echo "[✓] Install selesai untuk $INSTANCE!"
