# Project Case Study & Reflection

## Context

**Project:** SalesScope — Retail Sales Intelligence  
**Portfolio owner:** Ali Husnain  
**Engagement:** Independent learning and portfolio project, developed with AI assistance  
**Dataset:** Reproducible synthetic retail transactions; 5,197 lines across 2,600 orders

## Analytical objective

Translate transaction-level sales data into reliable, interpretable reporting. The project prioritizes accounting consistency and transparent evaluation over unsupported claims of predictive sophistication.

**Roman Urdu:** Focus ye hai ke numbers explainable hon, input errors visible hon aur business user samajh sake ke result kis calculation se bana hai.

## Design decisions

| Decision | Rationale | Trade-off |
|---|---|---|
| Separate analytics from UI | Calculations can be tested independently | Two modules must remain aligned |
| Reject malformed rows with reasons | Avoid silently replacing missing values with zero | Exclusions can bias totals if not reviewed |
| Retain duplicate candidates | Identical order lines may be legitimate | A source owner must confirm duplicates |
| Use rule-based customer segments | Business users can inspect each rule | Thresholds are not learned or validated |
| Start with a seasonal-naive forecast | Establish an understandable benchmark | Does not model holidays or promotions |
| Evaluate chronologically | Keeps held-out observations out of backtest predictions | One split is limited evidence |

## Evaluation

The test suite covers financial arithmetic, unique-order counting, input rejection, order consistency, duplicate treatment, formula-safe exports, segmentation and forecast holdout behavior. Streamlit smoke tests cover demo loading, empty filters and the upload landing state.

Forecast MAE and WAPE are calculated in the dashboard for the active selection. Scores should be read with their time range and data scope; they are not evidence of accuracy on unseen client data. Business impact has not been measured.

## Reflection

**What this implementation demonstrates:** modular Python, data validation, feature engineering, exploratory reporting, customer analytics, baseline evaluation and business communication.

**What needs further evidence:** extraction completeness, suitability of customer thresholds, multiple forecast backtests, real-world usability and performance on larger files.

**Roman Urdu:** Professional Data Science ka matlab sirf attractive charts nahi; data definitions, honest evaluation aur clear limitations bhi deliverable ka hissa hain.

## Next iteration

1. Agree on a real client's reporting definitions and acceptance criteria.
2. Support returns with an explicit transaction type and unique line IDs.
3. Compare forecasting candidates using rolling-origin evaluation.
4. Review segmentation thresholds against actual purchase cycles.
5. Add reviewed authentication and storage if confidential hosted use is required.

These are planned extensions, not existing features. This project does not claim paid client experience, production readiness or measured revenue improvement.
