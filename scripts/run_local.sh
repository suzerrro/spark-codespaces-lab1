#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
require_docker
app="${1:-apps/03_partition_workers.py}"
[[ "$app" == apps/*.py && "$app" != *..* && -f "$app" ]] || { echo '[ERROR] apps/ 안의 Python 파일을 지정하세요.' >&2; exit 2; }
shift || true
docker compose exec -T spark-client /opt/spark/bin/spark-submit \
  --master 'local[2]' --deploy-mode client --driver-memory 512m \
  --conf spark.driver.host=spark-client --conf spark.driver.bindAddress=0.0.0.0 \
  --conf spark.sql.shuffle.partitions=4 --conf spark.ui.port=4040 \
  "/lab/$app" "$@"
