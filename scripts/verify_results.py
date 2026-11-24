"""Check actual persisted outputs after running the Spark applications."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
expected=json.loads((ROOT/'data/expected.json').read_text())
def read(name):
    p=ROOT/'output'/name
    if not p.exists(): raise SystemExit(f'[FAIL] {p} 없음. 해당 실습 프로그램부터 실행하세요.')
    return json.loads(p.read_text())
a=read('orders_summary.json')
for k,v in a.items(): assert v==expected[k],k
for mode in ['cluster','local']:
    r=read('partitions_'+mode+'.json')
    assert r['total']==50005000
    assert len(r['partitions'])==8
    assert sum(x['count'] for x in r['partitions'])==10000
    if mode=='local': assert r['hosts']==['spark-client'],r['hosts']
    else: assert set(r['hosts']).issubset({'spark-worker-1','spark-worker-2'}),r['hosts']
from collections import Counter
assert read('wordcount.json')==dict(Counter((ROOT/'data/wordcount.txt').read_text().split()))
print('[PASS] orders / cluster partitions / local partitions / current wordcount')
