import argparse, time
from pyspark.sql import SparkSession
parser=argparse.ArgumentParser();parser.add_argument('--hold-seconds',type=int,default=0)
args=parser.parse_args()
spark=SparkSession.builder.appName('Lab01 Hello Spark').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
try:
    print('=== 실습 01 Spark 실행 확인 ===',flush=True)
    print('연결된 Master:',spark.sparkContext.master,flush=True)
    df=spark.range(1,101).repartition(4).selectExpr('id','id * 2 AS doubled')
    print('파티션 수:',df.rdd.getNumPartitions(),flush=True)
    n=df.count();print('Action 실행 count =',n,flush=True);assert n==100
    df.orderBy('id').show(10)
    print('Spark UI:',spark.sparkContext.uiWebUrl,flush=True)
    if args.hold_seconds:
        print('PORTS 4040에서 Jobs / Stages / Executors를 관찰하세요.',flush=True)
        time.sleep(max(0,min(args.hold_seconds,600)))
    print('[PASS] hello count=100',flush=True)
finally: spark.stop()
