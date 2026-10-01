# SalesScope | Retail Sales Intelligence

**Sales analytics · Customer segmentation · Forecast evaluation · Data quality**

An independent Data Science portfolio project by **Ali Husnain**, developed with AI assistance. SalesScope transforms order-line data into explainable business metrics, customer segments and an evaluated forecasting baseline.

**English:** Use the dashboard to investigate revenue drivers, margin leakage and customer purchasing patterns.

**Roman Urdu:** Is project ka maqsad sales data ko clear business insights mein convert karna hai, taake user revenue, gross profit aur customer behavior ko samajh sake.

[Roman Urdu + English setup guide](START_HERE.md) · [Project case study](CASE_STUDY.md)

> **Data disclosure:** The included 5,197 order lines and 2,600 orders are synthetic. This is independent portfolio work, not a paid client engagement or evidence of commercial impact.

## Business problem

Sales exports often show transactions without explaining which products drive revenue, where discounts reduce margins, or which customers return. SalesScope provides a reproducible workflow for investigating these questions.

| Business question | Analytical approach | Deliverable |
|---|---|---|
| What drives sales? | Time aggregation and product/region comparisons | Filterable performance dashboard |
| Where is margin being lost? | Unit economics and negative-profit checks | Gross-profit observations |
| Which customers purchase repeatedly? | Recency, frequency and monetary analysis | Rule-based customer segments |
| What is a reasonable short-term baseline? | Four-week seasonal-naive forecast | Forecast CSV and holdout error |
| Can the input be trusted? | Schema, range and order-consistency checks | Rejection log and duplicate warnings |

## Data Science workflow

1. **Define the data contract:** one row per order line, explicit dates and one currency.
2. **Validate inputs:** reject invalid records with reasons; preserve potentially legitimate duplicates for review.
3. **Engineer metrics:** calculate discounted revenue, cost of goods sold, gross profit and customer purchase summaries.
4. **Explore patterns:** compare time periods, products, regions and customer groups.
5. **Evaluate a baseline:** use a chronological holdout and report MAE/WAPE without using holdout sales in predictions.
6. **Communicate results:** present interpretable charts, downloadable tables and explicit assumptions.

**Technology:** Python, Pandas, NumPy, Plotly, Streamlit and pytest. No GPU, paid API or external model service is required.

## Features

- Interactive date, region and category filters; currency labels without conversion.
- Net sales, gross profit, orders and average order value, with equal-length prior-period comparisons when covered.
- Monthly trends, product/region/category performance and negative-profit observations.
- Customer recency/frequency/value analysis with transparent, configurable-in-code segment rules.
- Weekly baseline forecast with a four-week holdout MAE and WAPE.
- CSV schema validation, rejected-row reasons and duplicate-candidate reporting.
- Downloadable sales, customer segments, performance, forecast and executive text report.
- Separate analytics module and tests; no paid API or GPU required.

## Run locally (Windows)

Install Python 3.11 or 3.12. Extract this project, open its folder in VS Code and use the terminal:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On macOS/Linux activate using `source .venv/bin/activate` instead. Your terminal will show a local browser address, usually http://localhost:8501.

## Input contract

One CSV row = one order line. UTF-8 encoding, header row, at most 20 MB. All money values must use the same currency; changing the currency label does not convert values. IDs are read as strings so leading zeroes survive.

| Column | Meaning |
|---|---|
| order_id | Nonempty order ID; may repeat for multiple products |
| order_date | YYYY-MM-DD, e.g. 2026-09-30 |
| customer_id | Nonempty pseudonymous customer ID |
| product | Product name |
| category | Category name |
| region | Sales region |
| quantity | Positive integer |
| unit_price | Nonnegative price before discount |
| unit_cost | Nonnegative cost per unit |
| discount_pct | Percentage from 0 to 100, e.g. 10 means 10% |

All columns are required. Order lines sharing an order ID must agree on date, customer and region. Extra columns are ignored. Invalid rows are excluded and available in the rejection report. Exact duplicate candidates are retained, since the input has no unique line ID; investigate them before accepting totals. Returns and negative quantities are unsupported and rejected.

## Metric definitions

- Net sales = quantity × unit price × (1 − discount_pct / 100).
- Cost of goods sold = quantity × unit cost.
- Gross profit = net sales − cost of goods sold. This is **not net profit**: overhead, shipping and tax are excluded.
- Orders = distinct order IDs; AOV = filtered net sales / filtered distinct orders.
- Gross margin = gross profit / net sales; zero revenue produces a displayed 0 KPI (undefined product margins remain blank).
- Prior period is the immediately preceding equal number of calendar days, using the same region/category filters. Coverage is inferred from observed dataset boundaries, not independently verified.
- RFM-style segments use only filtered history; recency reference is one day after its final sale. The UI lists rule precedence. These are descriptive groups, not trained predictions.

## Forecast methodology & limits

Aggregate to Monday–Sunday weeks. Exclude boundary weeks that are not fully covered by the observed date span. Missing dates inside that span are assumed zero sales; confirm extraction completeness before forecasting. Require 12 complete weeks. Hold out the final four weeks and predict them with the preceding four weeks. Report mean absolute error and weighted absolute percentage error; WAPE is undefined if holdout revenue totals zero. For future dates, repeat the most recent four weeks.

This is a transparent seasonal-naive benchmark, not a validated production demand model. It has no confidence interval and does not incorporate promotions or holidays. Evaluate on longer real business history before operational use.

## Test

```sh
python -m pip install pytest
python -m pytest -q
```

`tests/test_analytics.py` checks accounting math, order counts, rejected records, duplicate policy, export safety, segmentation and forecast holdout behavior. `tests/test_app.py` exercises demo loading, empty filters and the upload landing screen.

## Project structure

- `app.py`: Streamlit interface and exports.
- `analytics.py`: validation and reusable business calculations.
- `generate_demo.py`: deterministic synthetic data generation (seed 42).
- `data/demo_sales.csv`: ready-to-run example.
- `data/sales_template.csv`: empty upload template.
- `tests/`: calculations and app smoke tests.
- `START_HERE.md`: Roman Urdu + professional English setup and demo guide.
- `CASE_STUDY.md`: business framing, design decisions, evaluation and project reflection.

## Repository & deployment

This project is organized under `salesscope-analytics/` in Ali Husnain's GitHub repository. After cloning or downloading the repository, open that project folder before running the setup commands.

Keep virtual environments, secrets and private client CSVs out of version control. For a later standalone repository, copy this project folder's contents to the new repository root.

For a hosted Streamlit deployment, use `app.py` as the entry point and install `requirements.txt`. This package has not been deployed. Authentication, roles, database storage and multi-tenant isolation are not implemented; add and review these before serving confidential client workloads. Uploaded bytes are processed in the Streamlit session; the app does not intentionally persist uploads or send them to external APIs.

## Honest portfolio positioning

Describe this as an independent portfolio project using synthetic retail data. Demonstrate the business question, cleaning decisions, formulas and limitations. Do not claim real client outcomes. Validate a client's data definitions, currency, returns, taxes and reporting dates before adapting the project.
