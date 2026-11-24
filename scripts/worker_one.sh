#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
require_docker
docker compose stop spark-worker-2
bash scripts/check_cluster.sh 1
bash scripts/run.sh apps/03_partition_workers.py
