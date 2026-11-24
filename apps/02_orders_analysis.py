import json
from pathlib import Path
from pyspark.sql import SparkSession, functions as F, types as T
spark=SparkSession.builder.appName('Lab02 Orders Analysis').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
try:
    schema=T.StructType([T.StructField(n,t,False) for n,t in [
        ('order_id',T.StringType()),('order_date',T.StringType()),('region',T.StringType()),
        ('category',T.StringType()),('channel',T.StringType()),('quantity',T.IntegerType()),
        ('unit_price',T.IntegerType()),('order_amount',T.LongType()),('status',T.StringType())]])
    df=spark.read.option('header',True).schema(schema).csv('/lab/data/orders.csv')
    df.printSchema();df.show(5,truncate=False)
    statuses={r['status']:r['count'] for r in df.groupBy('status').count().collect()}
    paid=df.filter(F.col('status')=='PAID')
    revenue=paid.groupBy('region').agg(F.sum('order_amount').alias('revenue'))
    revenue.orderBy(F.desc('revenue')).show()
    df.createOrReplaceTempView('orders')
    sql=spark.sql("SELECT region, SUM(order_amount) AS revenue FROM orders WHERE status='PAID' GROUP BY region")
    sql.orderBy(F.desc('revenue')).show();sql.explain(mode='formatted')
    region={r['region']:r['revenue'] for r in revenue.collect()}
    sql_region={r['region']:r['revenue'] for r in sql.collect()}
    category_df=paid.groupBy('category').agg(F.sum('order_amount').alias('revenue'))
    # 과제 A: 아래 예시를 참고해 channel별 결제 완료 거래액을 추가하세요.
    category_df.orderBy(F.desc('revenue')).show()
    category={r['category']:r['revenue'] for r in category_df.collect()}
    actual=dict(rows=df.count(),status=statuses,paid_by_region=region,paid_by_category=category)
    expected=json.loads(Path('/lab/data/expected.json').read_text())
    for k,v in actual.items(): assert v==expected[k],(k,v,expected[k])
    assert region==sql_region,'DataFrame/SQL 결과 불일치'
    Path('/lab/output/orders_summary.json').write_text(json.dumps(actual,indent=2)+'\n')
    print('[PASS] orders: 2400 rows, status counts, region/category revenue, SQL parity',flush=True)
finally: spark.stop()
