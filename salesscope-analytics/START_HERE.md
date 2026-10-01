# Getting Started | Roman Urdu + Professional English

**SalesScope — Retail Sales Intelligence**  
Independent Data Science portfolio project by Ali Husnain, developed with AI assistance.

## 1. Project overview — Ye project kya karta hai?

SalesScope aapke sales CSV ko interactive dashboard mein convert karta hai. Aap revenue trends, gross profit, product performance aur customer purchasing patterns analyze kar sakte hain.

**Professional description:** “A sales analytics application with auditable business metrics, rule-based customer segmentation and an evaluated forecasting baseline.”

## 2. Installation — Project kaise run karein?

Python 3.11 ya 3.12 install karein. GitHub se project download karke `salesscope-analytics` folder VS Code mein open karein. Agar purana ZIP use kar rahe hain to folder ka naam `salesscope` ho sakta hai.

Windows terminal mein ye commands aik aik karke run karein:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**Expected result:** Terminal mein local browser address nazar aayega; usay open karne par synthetic demo dashboard load hoga. GPU ya paid API ki zaroorat nahi.

Agar PowerShell activation block kare, environment activate kiye baghair ye commands use karein:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

## 3. Dashboard walkthrough — Har section ka purpose

| Section | Professional purpose | Roman Urdu explanation |
|---|---|---|
| Overview | Monitor sales and gross profit | Sales trend aur gross profit aik jagah dekhein |
| Products & regions | Compare commercial performance | Konsa product ya region zyada revenue contribute karta hai |
| Customer segments | Summarize purchasing behavior | Repeat buyers aur less-recent customers identify karein |
| Forecast | Evaluate a short-term baseline | Estimated weekly sales ke saath historical prediction error dekhein |
| Data quality | Audit input reliability | Invalid rows aur possible duplicates review karein |

## 4. Upload your data — Apna CSV use karein

Sidebar mein **Upload CSV** select karein aur template download karein. Column names template ke mutabiq rakhein. Dates `YYYY-MM-DD`, quantity positive whole number aur discount `0–100` hona chahiye.

**Important distinction:** Currency dropdown sirf label change karta hai; exchange-rate conversion nahi karta. Gross profit mein overhead, tax aur shipping include nahi hote. Returns is version mein supported nahi hain.

## 5. Professional demo — Client ko kaise explain karein?

**Opening:** “SalesScope brings sales performance, customer behavior and data-quality checks into one analytical workflow.”

Roman Urdu mein: “Is dashboard se aap dekh sakte hain ke sales kahan se aa rahi hain, margins kahan weak hain aur customers ka buying pattern kya hai.”

1. **Scope:** Date, region aur category filters change karke reporting context explain karein.
2. **Performance:** Revenue aur gross profit ka difference samjhayein.
3. **Diagnosis:** Products tab mein low-margin items investigate karein.
4. **Customers:** Segments ke rules explain karein; inhein churn prediction na kahein.
5. **Forecast:** “This is a transparent benchmark with a historical holdout evaluation, not guaranteed future sales.”
6. **Delivery:** CSV aur summary report export karke dikhayein.

**Data disclosure:** “This demonstration uses synthetic data. Real business data would require validation and adaptation to your reporting definitions.”

## 6. Client discovery — Kaam start karne se pehle

- **Business objective:** Aap kaunsa decision improve karna chahte hain?
- **Data structure:** Har row order hai ya order line? Export kis system se aata hai?
- **Accounting definitions:** Discounts, costs, returns aur taxes kaise record hote hain?
- **Reporting scope:** Currency, reporting period aur required refresh frequency kya hai?
- **Access requirements:** Dashboard kaun use karega aur data kitna confidential hai?

## 7. Learning path — Code kis order mein samjhein?

Pehle `analytics.py` mein `clean()` aur `kpis()` padhein. Phir `customers()` ke rules aur `forecast()` ki holdout logic samjhein. Aakhir mein `app.py` dekhein ke ye functions interface ke saath kaise connect hote hain.

Client discussion se pehle aapko formulas, assumptions aur limitations apne words mein explain karne aane chahiye. Sirf dashboard run karna project understanding ka substitute nahi hai.
