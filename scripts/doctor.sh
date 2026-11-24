#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
printf 'Repository: %s\n' "$LAB_ROOT"
test -f .devcontainer/devcontainer.json || { echo '[ERROR] .devcontainer 누락'; exit 1; }
require_docker
docker compose config -q
python3 --version
docker compose version
docker compose ps
printf '\n[OK] Docker Client/Server와 Compose 설정을 확인했습니다.\n'
