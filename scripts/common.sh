#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$LAB_ROOT"
require_docker() {
  command -v docker >/dev/null || { echo '[ERROR] docker 명령이 없습니다. .devcontainer 파일과 복구 모드 여부를 확인하세요.' >&2; return 1; }
  docker compose version >/dev/null || { echo '[ERROR] Docker Compose v2가 없습니다. Dev Container를 Rebuild하세요.' >&2; return 1; }
  docker info >/dev/null 2>&1 || { echo '[ERROR] Docker Server에 연결할 수 없습니다. 30초 후 재시도하고 계속 실패하면 Rebuild Container하세요.' >&2; return 1; }
}
