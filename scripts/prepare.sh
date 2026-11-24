#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p output logs
chmod a+rwx output
if [[ ! -f data/orders.csv ]]; then python3 scripts/generate_data.py; fi
printf '\n[준비 완료] Docker 이미지는 아직 다운로드하지 않았습니다.\n다음 명령: bash scripts/start.sh\n'
