#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
require_docker
docker compose start spark-worker-2
bash scripts/check_cluster.sh 2
