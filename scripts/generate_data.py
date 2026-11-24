"""Generate the versioned synthetic teaching fixture and its independent answers."""
import csv, json, random
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    rng=random.Random(42)
    statuses=['PAID']*2026+['CANCELLED']*248+['REFUNDED']*126
    rng.shuffle(statuses)
    rows=[]
    for i,status in enumerate(statuses,1):
        region=rng.choice(['Seoul','Busan','Incheon','Daegu','Daejeon'])
        category=rng.choice(['Books','Electronics','Food','Clothing'])
        quantity=rng.randint(1,5)
        unit_price=rng.choice([5000,10000,15000,20000,35000,50000])
        rows.append(dict(order_id=f'O{i:05d}',order_date=str(date(2026,1,1)+timedelta(days=rng.randrange(90))),region=region,category=category,channel=rng.choice(['Web','App']),quantity=quantity,unit_price=unit_price,order_amount=quantity*unit_price,status=status))
    data=ROOT/'data'; data.mkdir(exist_ok=True)
    with (data/'orders.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    text='spark hadoop spark sql\nspark python data engineering\nhadoop data spark\npython sql data\n'
    (data/'wordcount.txt').write_text(text,encoding='utf-8')
    region=defaultdict(int);category=defaultdict(int)
    for r in rows:
        if r['status']=='PAID':
            region[r['region']]+=r['order_amount'];category[r['category']]+=r['order_amount']
    expected=dict(rows=len(rows),status=dict(Counter(r['status'] for r in rows)),paid_by_region=dict(sorted(region.items())),paid_by_category=dict(sorted(category.items())),wordcount=dict(sorted(Counter(text.split()).items())),partition_sum=50005000)
    (data/'expected.json').write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(expected,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
