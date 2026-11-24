#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
bash scripts/prepare.sh
require_docker
docker compose config -q
echo '[1/3] Spark 이미지 다운로드'
docker compose pull
echo '[2/3] Master, Worker 2개, Client 시작'
docker compose up -d
echo '[3/3] Worker 2개 등록 확인'
bash scripts/check_cluster.sh 2
