from pathlib import Path
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from analytics import clean, kpis, customers, forecast, safe_csv, REQUIRED

st.set_page_config(page_title='SalesScope | Retail Sales Intelligence',page_icon='📊',layout='wide')
st.markdown('''<style>.block-container{padding-top:2rem}h1{letter-spacing:-1.5px}[data-testid="stMetric"]{background:white;border:1px solid #e1e8ee;padding:18px;border-radius:12px}[data-testid="stMetricValue"]{font-size:1.8rem}</style>''',unsafe_allow_html=True)
st.sidebar.title('◈ SalesScope')
st.sidebar.caption('RETAIL SALES INTELLIGENCE')
source=st.sidebar.radio('Data source',['Synthetic demo','Upload CSV'])
currency=st.sidebar.selectbox('Currency label (no conversion)',['PKR','USD','EUR','GBP','AED'])
if source=='Upload CSV':
    upload=st.sidebar.file_uploader('Sales order lines • CSV',type=['csv'])
    st.sidebar.download_button('Download CSV template',(','.join(REQUIRED)+'\n').encode(),'sales_template.csv','text/csv')
    if upload is None:
        st.title('Bring your sales into focus')
        st.info('Upload a CSV using the template. One row per order line; dates YYYY-MM-DD; discount_pct from 0 to 100. All amounts must use one currency.')
        st.stop()
    try:
        raw=pd.read_csv(io.BytesIO(upload.getvalue()),dtype='string',keep_default_na=False)
    except (ValueError,UnicodeError,pd.errors.ParserError,pd.errors.EmptyDataError):
        st.error('Could not read the CSV. Save it as UTF-8 CSV with a header row.');st.stop()
else:
    raw=pd.read_csv(Path(__file__).parent/'data/demo_sales.csv',dtype='string',keep_default_na=False)
try:
    data,rejected,duplicates=clean(raw)
except ValueError as e:
    st.error(str(e));st.stop()
if data.empty:
    st.error('No valid sales rows. Review the rejected rows below.')
    st.dataframe(rejected)
    st.download_button('Download rejected rows',safe_csv(rejected),'rejected_rows.csv');st.stop()

st.sidebar.divider()
dates=st.sidebar.date_input('Analysis period',value=(data.order_date.min().date(),data.order_date.max().date()),min_value=data.order_date.min().date(),max_value=data.order_date.max().date())
regions=st.sidebar.multiselect('Regions',sorted(data.region.unique()),default=sorted(data.region.unique()))
categories=st.sidebar.multiselect('Categories',sorted(data.category.unique()),default=sorted(data.category.unique()))
if len(dates)!=2:
    st.info('Choose both a start and end date.');st.stop()
start,end=map(pd.Timestamp,dates)
mask=data.region.isin(regions)&data.category.isin(categories)
filtered=data[mask & data.order_date.between(start,end)]
length=(end-start).days+1
previous=data[mask & data.order_date.between(start-pd.Timedelta(days=length),start-pd.Timedelta(days=1))]
full_previous=start-pd.Timedelta(days=length)>=data.order_date.min()
st.title('Sales performance, made clear.')
st.caption(f'{start:%d %b %Y} — {end:%d %b %Y}  ·  {currency}  ·  '+('SYNTHETIC DEMO DATA' if source=='Synthetic demo' else 'UPLOADED DATA'))
if rejected.shape[0]:st.warning(f'{len(rejected):,} invalid rows excluded. Open Data quality for details.')
if filtered.empty:
    st.info('No sales match these filters. Expand the date range or select more categories/regions.');st.stop()
k=kpis(filtered);p=kpis(previous)
cols=st.columns(4)
for col,key,label,fmt in zip(cols,['revenue','profit','orders','aov'],['Net sales','Gross profit','Orders','Average order value'],[',.0f',',.0f',',d',',.0f']):
    delta=f'{(k[key]/p[key]-1)*100:+.1f}% vs prior period' if full_previous and p[key]!=0 else None
    col.metric(label,format(k[key],fmt),delta)
st.caption(f'Gross margin {k["margin"]:.1f}% · {k["customers"]:,} purchasing customers · Gross profit excludes overhead, tax and shipping. Order values reflect selected categories only.')
if not full_previous:st.caption('Prior-period comparison unavailable: the dataset does not cover the full preceding interval.')

def chart(fig):
    fig.update_layout(template='plotly_white',font=dict(family='Arial',color='#13263C'),margin=dict(l=10,r=10,t=40,b=10),paper_bgcolor='rgba(0,0,0,0)',colorway=['#0D9488','#2563EB','#F59E0B','#7C3AED'])
    st.plotly_chart(fig,use_container_width=True)

overview,products,people,future,quality=st.tabs(['Overview','Products & regions','Customer segments','Forecast','Data quality'])
with overview:
    monthly=filtered.set_index('order_date')[['revenue','gross_profit']].resample('MS').sum().reset_index()
    chart(px.line(monthly,x='order_date',y=['revenue','gross_profit'],markers=True,title='Monthly net sales & gross profit',labels={'value':currency,'order_date':'Month','variable':'Metric'}))
    left,right=st.columns([1,1])
    with left:
        cat=filtered.groupby('category',as_index=False).revenue.sum().sort_values('revenue')
        chart(px.bar(cat,x='revenue',y='category',orientation='h',title='Revenue by category'))
    with right:
        st.subheader('Business observations')
        best=cat.iloc[-1]
        share=100*best.revenue/k['revenue'] if k['revenue'] else 0
        st.info(f'{best.category} contributes {share:.1f}% of net sales. Review stock availability for its leading products.')
        loss=filtered[filtered.gross_profit<0]
        st.warning(f'{len(loss):,} order lines have negative gross profit. Review their discounts and unit costs.') if len(loss) else st.success('No negative gross-profit lines in this selection.')
        st.write(f'Total discounts: {currency} {filtered.discount_value.sum():,.0f}. Compare discount campaigns against gross profit, not revenue alone.')
    st.download_button('Export filtered sales',safe_csv(filtered),'filtered_sales.csv','text/csv')
    report=f'SalesScope report\nPeriod: {start.date()} to {end.date()}\nSource: {source}\nCurrency: {currency}\nRegions: {", ".join(regions)}\nCategories: {", ".join(categories)}\n'+ '\n'.join(f'{key}: {val:,.2f}' for key,val in k.items())+'\nGross profit excludes overhead, tax and shipping.\n'
    st.download_button('Download summary report',report,'sales_summary.txt','text/plain')
with products:
    group=st.selectbox('Analyze by',['product','region','category'])
    table=filtered.groupby(group).agg(revenue=('revenue','sum'),gross_profit=('gross_profit','sum'),units=('quantity','sum'),orders=('order_id','nunique')).reset_index()
    table['margin_pct']=(table.gross_profit/table.revenue.where(table.revenue.ne(0))*100).round(2)
    table=table.sort_values('revenue',ascending=False)
    chart(px.bar(table.head(15),x=group,y=['revenue','gross_profit'],barmode='group',title='Top performers'))
    st.dataframe(table,use_container_width=True,hide_index=True)
    st.download_button('Export performance table',safe_csv(table),'performance.csv','text/csv')
with people:
    r=customers(filtered)
    st.caption('RFM-style rules within selected data. Recency is measured from the day after the latest selected sale; frequency counts distinct orders. This is a descriptive segmentation, not a churn prediction.')
    a,b=st.columns([1,2])
    with a:chart(px.pie(r,names='segment',hole=.65,title='Customer mix'))
    with b:chart(px.scatter(r,x='recency_days',y='monetary',size='frequency',color='segment',hover_data=['customer_id'],title='Recency × customer value'))
    with st.expander('Segment definitions'):
        st.write('Loyal & active: recency ≤30 days and ≥3 orders. Win-back: recency >90 days. One-time: 1 order among remaining customers. Developing: all remaining customers. Rules run in this order.')
    st.dataframe(r.sort_values('monetary',ascending=False),hide_index=True,use_container_width=True)
    st.download_button('Export customer segments',safe_csv(r),'customer_segments.csv','text/csv')
with future:
    st.subheader('A transparent sales baseline')
    st.caption('Repeats the last four complete weeks. Not an AI promise: promotions, holidays and business changes are not modeled. In-range missing dates count as zero; incomplete boundary weeks are excluded.')
    horizon=st.slider('Weeks ahead',1,12,4)
    try:
        history,prediction,mae,wape=forecast(filtered,horizon)
        a,b=st.columns(2);a.metric('Holdout MAE per week',f'{currency} {mae:,.0f}');b.metric('Holdout WAPE','N/A (zero actual sales)' if wape is None else f'{wape:.1f}%')
        st.caption('Backtest: predict the final 4 complete weeks using the preceding 4; no holdout values used for those predictions. This single split does not establish future accuracy.')
        fig=go.Figure();fig.add_scatter(x=history.index,y=history.values,name='Observed',line_color='#0D9488');fig.add_scatter(x=prediction.week,y=prediction.forecast,name='Baseline forecast',line=dict(color='#7C3AED',dash='dash'))
        chart(fig)
        st.download_button('Export forecast',safe_csv(prediction),'weekly_forecast.csv','text/csv')
    except ValueError as e:st.info(str(e))
with quality:
    a,b,c=st.columns(3);a.metric('Source rows',len(raw));b.metric('Rejected rows',len(rejected));c.metric('Exact duplicate candidates',duplicates)
    st.caption('Quality checks cover the full input before filters. Duplicate candidates remain included because identical order lines may be legitimate. Confirm them with the source owner.')
    if duplicates:st.warning('Potential duplicates affect totals. Review matching source records before using the results.')
    st.dataframe(rejected,hide_index=True,use_container_width=True)
    st.download_button('Export rejection log',safe_csv(rejected),'rejected_rows.csv','text/csv')
    st.write('Required columns: '+', '.join(REQUIRED))
    st.caption('Revenue = quantity × unit price × (1 − discount/100). Gross profit = revenue − quantity × unit cost. Returns/negative quantities are rejected; this model is for completed positive sales only.')
st.sidebar.divider()
st.sidebar.caption('Ali Husnain · Portfolio edition · v1.1\nUploads are processed in the app session; this app does not save uploaded files to disk.')
