"""Auditable sales metrics. All money inputs must use one currency."""
import numpy as np
import pandas as pd

REQUIRED = ['order_id','order_date','customer_id','product','category','region','quantity','unit_price','unit_cost','discount_pct']

def clean(raw):
    d = raw.copy()
    d.columns = d.columns.str.strip().str.lower()
    if d.columns.duplicated().any():
        raise ValueError('Duplicate column names. Give every column a unique name.')
    missing = set(REQUIRED) - set(d.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    d = d[REQUIRED].copy()
    reasons = pd.Series('', index=d.index)
    def flag(mask, reason):
        reasons.loc[mask] += reason + '; '
    for c in ['order_id','customer_id','product','category','region']:
        d[c] = d[c].astype('string').str.strip()
        flag(d[c].isna() | d[c].eq(''), 'Missing '+c)
    dates = d.order_date.astype('string')
    d['order_date'] = pd.to_datetime(dates.where(dates.str.fullmatch(r'\d{4}-\d{2}-\d{2}', na=False)), format='%Y-%m-%d', errors='coerce')
    flag(d.order_date.isna(), 'Invalid date (use YYYY-MM-DD)')
    for c in ['quantity','unit_price','unit_cost','discount_pct']:
        d[c] = pd.to_numeric(d[c], errors='coerce')
        flag(~np.isfinite(d[c]), 'Invalid '+c)
    flag((d.quantity <= 0) | (d.quantity % 1 != 0), 'Quantity must be a positive whole number')
    flag((d.unit_price < 0) | (d.unit_cost < 0), 'Negative price/cost')
    flag(~d.discount_pct.between(0,100), 'Discount must be 0–100')
    # An order may contain multiple products, but must have one date/customer/region.
    bad_orders = d.groupby('order_id')[['order_date','customer_id','region']].nunique().gt(1).any(axis=1)
    flag(d.order_id.isin(bad_orders[bad_orders].index), 'Conflicting order metadata')
    rejected = raw.loc[reasons.ne('')].copy()
    rejected['rejection_reason'] = reasons[reasons.ne('')]
    d = d.loc[reasons.eq('')].copy()
    duplicates = int(d.duplicated().sum())
    # Preserve exact matches: identical lines may be legitimate order lines.
    d['gross_sales'] = d.quantity * d.unit_price
    d['discount_value'] = d.gross_sales * d.discount_pct / 100
    d['revenue'] = d.gross_sales - d.discount_value
    d['cogs'] = d.quantity * d.unit_cost
    d['gross_profit'] = d.revenue - d.cogs
    return d, rejected, duplicates

def kpis(d):
    revenue = float(d.revenue.sum())
    orders = int(d.order_id.nunique())
    profit = float(d.gross_profit.sum())
    return dict(revenue=revenue, profit=profit, orders=orders, customers=int(d.customer_id.nunique()),
                aov=revenue/orders if orders else 0, margin=100*profit/revenue if revenue else 0)

def customers(d):
    if d.empty:
        return pd.DataFrame()
    reference = d.order_date.max() + pd.Timedelta(days=1)
    r = d.groupby('customer_id').agg(last_purchase=('order_date','max'),frequency=('order_id','nunique'),monetary=('revenue','sum'),profit=('gross_profit','sum'))
    r['recency_days'] = (reference-r.last_purchase).dt.days
    r['segment'] = np.select([
        (r.recency_days <= 30) & (r.frequency >= 3),
        r.recency_days > 90,
        r.frequency == 1], ['Loyal & active','Win-back candidates','One-time buyers'], default='Developing')
    return r.reset_index()

def forecast(d, horizon=4):
    """Weekly seasonal-naive baseline; last partial weeks excluded.
    Last 4 complete weeks held out for honest error measurement.
    Missing days within the observed span are assumed zero sales.
    """
    if d.empty:
        raise ValueError('No data to forecast.')
    daily = d.groupby('order_date').revenue.sum().asfreq('D', fill_value=0)
    weeks = daily.resample('W-SUN').sum()
    weeks = weeks[(weeks.index-pd.Timedelta(days=6) >= daily.index.min()) & (weeks.index <= daily.index.max())]
    if len(weeks) < 12:
        raise ValueError('Forecast needs at least 12 complete weeks in the selected data.')
    actual = weeks.iloc[-4:].to_numpy()
    predicted = weeks.iloc[-8:-4].to_numpy()
    mae = float(np.abs(actual-predicted).mean())
    denom = np.abs(actual).sum()
    wape = float(np.abs(actual-predicted).sum()/denom*100) if denom else None
    future = np.resize(weeks.iloc[-4:].to_numpy(), horizon)
    dates = pd.date_range(weeks.index[-1]+pd.Timedelta(days=7), periods=horizon, freq='W-SUN')
    return weeks, pd.DataFrame({'week':dates,'forecast':future}), mae, wape

def safe_csv(d):
    """Escape spreadsheet formula prefixes in text exports."""
    out = d.copy()
    for c in out.select_dtypes(include=['object','string']).columns:
        out[c] = out[c].map(lambda v: "'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@','\t','\r','\n')) else v)
    return out.to_csv(index=False).encode('utf-8-sig')
