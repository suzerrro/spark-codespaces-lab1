#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
bash scripts/check_cluster.sh 2
for app in apps/01_hello_spark.py apps/02_orders_analysis.py apps/03_partition_workers.py apps/04_wordcount.py; do
  bash scripts/run.sh "$app" 2>&1 | tee "logs/$(basename "$app" .py).log"
done
bash scripts/run_local.sh apps/03_partition_workers.py 2>&1 | tee logs/local_partitions.log
python3 scripts/verify_results.py
