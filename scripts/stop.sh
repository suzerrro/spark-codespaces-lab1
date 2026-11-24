#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
require_docker
docker compose down
echo '[중요] github.com/codespaces 에서 이 Codespace 자체도 Stop하세요. 브라우저 탭만 닫으면 중지되지 않을 수 있습니다.'
