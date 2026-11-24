import json, os, socket, time
from pathlib import Path
from pyspark.sql import SparkSession

def inspect_partition(index,values):
    values=list(values)
    time.sleep(2)  # 작은 데이터에서도 두 Worker가 Task를 받을 시간을 확보
    yield (index,socket.gethostname(),os.getpid(),len(values),sum(values))

if __name__=='__main__':
    spark=SparkSession.builder.appName('Lab03 Partitions and Workers').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    try:
        sc=spark.sparkContext
        rows=sc.parallelize(range(1,10001),8).mapPartitionsWithIndex(inspect_partition).collect()
        rows.sort()
        print('Master:',sc.master,flush=True)
        print('partition | host | pid | count | sum',flush=True)
        for r in rows: print(' | '.join(map(str,r)),flush=True)
        total=sum(r[4] for r in rows);hosts=sorted({r[1] for r in rows})
        assert len(rows)==8 and sum(r[3] for r in rows)==10000 and total==50005000
        print('전체 합계:',total,flush=True);print('사용된 실행 호스트:',hosts,flush=True)
        mode='local' if sc.master.startswith('local') else 'cluster'
        if mode=='cluster' and len(hosts)<2:
            print('[관찰] 한 호스트만 사용했습니다. Worker 상태와 자원 사용량을 확인하세요.',flush=True)
        report=dict(master=sc.master,partitions=[dict(zip(['partition','host','pid','count','sum'],r)) for r in rows],hosts=hosts,total=total)
        Path('/lab/output/partitions_'+mode+'.json').write_text(json.dumps(report,indent=2)+'\n')
        print('[PASS] partitions=8 rows=10000 sum=50005000',flush=True)
    finally: spark.stop()
