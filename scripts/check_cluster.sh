#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
require_docker
expected="${1:-2}"
[[ "$expected" =~ ^[12]$ ]] || { echo '사용법: bash scripts/check_cluster.sh 1 또는 2'; exit 2; }
for ((i=1; i<=60; i++)); do
  if docker compose exec -T spark-client python3 - "$expected" <<'PY'
import json, sys, urllib.request
try:
    with urllib.request.urlopen('http://spark-master:8080/json/', timeout=3) as r:
        state=json.load(r)
    alive=[w for w in state.get('workers',[]) if w.get('state')=='ALIVE']
    print('등록된 활성 Worker:', len(alive), '/', sys.argv[1])
    if len(alive) != int(sys.argv[1]): sys.exit(1)
    for w in alive: print(w.get('host'), 'cores=',w.get('cores'),'memory=',w.get('memory'))
except Exception as exc:
    print('대기 중:', str(exc)); sys.exit(1)
PY
  then
    echo '[OK] 클러스터 준비 완료. PORTS 탭의 8080을 여세요.'
    exit 0
  fi
  sleep 2
done
echo '[ERROR] Worker 등록 시간 초과. 아래 로그를 확인하세요.' >&2
docker compose ps
docker compose logs --tail=60 spark-master spark-worker-1 spark-worker-2
exit 1
