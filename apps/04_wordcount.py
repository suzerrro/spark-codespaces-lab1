import json
from pathlib import Path
from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('Lab04 RDD WordCount').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
try:
    counts=(spark.sparkContext.textFile('/lab/data/wordcount.txt',minPartitions=4)
            .flatMap(lambda line:line.split()).map(lambda word:(word,1)).reduceByKey(lambda a,b:a+b))
    actual=dict(counts.collect())
    for word,n in sorted(actual.items()): print(word,n,flush=True)
    # Text is intentionally editable. Derive current expected values independently.
    from collections import Counter
    expected=dict(Counter(Path('/lab/data/wordcount.txt').read_text().split()))
    assert actual==expected,(actual,expected)
    Path('/lab/output/wordcount.json').write_text(json.dumps(actual,indent=2)+'\n')
    counts.sortByKey().saveAsTextFile('/lab/output/wordcount-'+str(__import__('time').time_ns()))
    print('[PASS] wordcount matches current input',flush=True)
finally: spark.stop()
