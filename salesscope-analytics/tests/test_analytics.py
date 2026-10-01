import pandas as pd
import pytest
from analytics import clean,kpis,forecast,safe_csv,REQUIRED,customers

def sample():
    return pd.DataFrame([['001','2026-01-01','C1','A','Tools','Lahore',2,100,60,10],['001','2026-01-01','C1','B','Tools','Lahore',1,50,20,0]],columns=REQUIRED)

def test_totals_and_distinct_orders():
    d,bad,_=clean(sample()); k=kpis(d)
    assert bad.empty
    assert k['revenue']==230 and k['profit']==90 and k['orders']==1 and k['aov']==230

def test_reject_invalid_not_silent_zero():
    raw=sample().astype(object);raw.loc[0,'unit_price']='oops'
    d,bad,_=clean(raw)
    assert len(bad)==1 and d.revenue.sum()==50

def test_conflicting_order_rejected():
    raw=sample();raw.loc[1,'customer_id']='C2'
    d,bad,_=clean(raw)
    assert d.empty and len(bad)==2

def test_duplicates_preserved_and_flagged():
    raw=sample().iloc[[0,0]].reset_index(drop=True)
    d,_,duplicates=clean(raw)
    assert duplicates==1 and len(d)==2

def test_returns_and_inf_rejected():
    raw=sample().astype(object);raw.loc[0,'quantity']=-1;raw.loc[1,'unit_cost']=float('inf')
    d,bad,_=clean(raw);assert d.empty and len(bad)==2

def test_dates_strict():
    raw=sample();raw.loc[0,'order_date']='01/02/2026'
    d,bad,_=clean(raw);assert len(bad)==1

def test_forecast_holdout():
    dates=pd.date_range('2026-01-05',periods=16*7)
    d=pd.DataFrame({'order_date':dates,'revenue':[10]*84+[20]*28})
    history,f,mae,wape=forecast(d)
    assert len(history)==16 and mae==70 and wape==50
    assert f.forecast.tolist()==[140]*4
    assert f.week.min()>history.index.max()

def test_short_forecast():
    with pytest.raises(ValueError):forecast(pd.DataFrame({'order_date':pd.date_range('2026-01-01',periods=5),'revenue':[10]*5}))

def test_export_formula():
    assert "'=cmd" in safe_csv(pd.DataFrame({'product':['=cmd']})).decode('utf-8-sig')

def test_rfm_order_not_lines():
    d,_,_=clean(sample());r=customers(d)
    assert r.frequency.iloc[0]==1 and r.segment.iloc[0]=='One-time buyers'
