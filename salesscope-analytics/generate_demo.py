"""Reproducible synthetic portfolio dataset; no real customer information."""
from pathlib import Path
import numpy as np
import pandas as pd
rng = np.random.default_rng(42)
products = [('Wireless Mouse','Electronics',3200,2050),('Desk Lamp','Home',4800,2900),('Notebook Set','Stationery',950,420),('Backpack','Accessories',6500,4100),('USB Hub','Electronics',4500,2850),('Water Bottle','Accessories',1800,800)]
rows=[]
for i in range(2600):
    date=pd.Timestamp('2025-01-01')+pd.Timedelta(days=int(rng.integers(0,638)))
    customer=f'C{int(rng.integers(1,401)):04}'
    region=rng.choice(['Lahore','Karachi','Islamabad','Faisalabad'])
    for p in rng.choice(len(products),size=int(rng.integers(1,4)),replace=False):
        product,category,price,cost=products[p]
        rows.append([f'ORD{i+1:05}',date.date(),customer,product,category,region,int(rng.integers(1,5)),price,cost,int(rng.choice([0,0,5,10,15,25,45]))])
from analytics import REQUIRED
path=Path(__file__).parent/'data'/'demo_sales.csv'
pd.DataFrame(rows,columns=REQUIRED).to_csv(path,index=False)
print(f'Created {len(rows)} synthetic order lines')
