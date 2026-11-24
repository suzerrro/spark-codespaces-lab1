#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
require_docker
app="${1:-apps/01_hello_spark.py}"
[[ "$app" == apps/*.py && "$app" != *..* && -f "$app" ]] || { echo '[ERROR] apps/ 안의 Python 파일을 지정하세요.' >&2; exit 2; }
shift || true
docker compose exec -T spark-client /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 --deploy-mode client \
  --driver-memory 512m --executor-memory 512m --executor-cores 1 \
  --conf spark.cores.max=2 --conf spark.dynamicAllocation.enabled=false \
  --conf spark.driver.host=spark-client --conf spark.driver.bindAddress=0.0.0.0 \
  --conf spark.driver.port=39001 --conf spark.blockManager.port=39002 \
  --conf spark.sql.shuffle.partitions=4 --conf spark.default.parallelism=4 \
  --conf spark.ui.port=4040 \
  "/lab/$app" "$@"
