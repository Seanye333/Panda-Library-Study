"""
Injects real-world use-case blocks into every topic in index.html,
and appends real-world example cells to the Jupyter notebook.
"""

import json, re

BASE = r"c:\Users\seany\Documents\All Codes\Python Panda Library Study"
HTML_FILE = BASE + r"\index.html"
NB_FILE   = BASE + r"\pandas_study_guide.ipynb"

# ── helpers ──────────────────────────────────────────────────────────────────
def escape(code):
    return code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rw(title, scenario, code):
    return (
        f'\n      <div class="rw-block">'
        f'\n        <div class="rw-header">&#128205; Real-World Use Case &mdash; {title}</div>'
        f'\n        <div class="rw-desc">{scenario}</div>'
        f'\n        <div class="code-block">'
        f'\n          <div class="code-label"><span>use-case example</span>'
        f'<button class="copy-btn" onclick="copyCode(this)">Copy</button></div>'
        f'\n          <pre><code class="language-python">{escape(code)}</code></pre>'
        f'\n        </div>'
        f'\n      </div>'
    )

def nb_code(src, cid):
    return {"cell_type":"code","execution_count":None,"id":cid,
            "metadata":{},"outputs":[],"source":src}

def nb_md(src, cid):
    return {"cell_type":"markdown","id":cid,"metadata":{},"source":src}

# ── Real-world examples ───────────────────────────────────────────────────────
RW = {}

RW["t1"] = rw(
"Setting Up a Data Analysis Project",
"A junior analyst at a retail company sets up their Python environment before analysing 12 months of sales data.",
"""\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Helpful display settings for wide DataFrames
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 100)
pd.set_option("display.float_format", "{:,.2f}".format)
pd.set_option("display.width", 120)

print(f"pandas {pd.__version__}  |  numpy {np.__version__}")
print("Environment ready for sales analysis.")""")

RW["t2"] = rw(
"Daily Stock Price Tracker",
"<strong>Scenario:</strong> A quant stores 10 days of AAPL closing prices and needs daily returns, best/worst day, and annualised volatility.",
"""\
import pandas as pd

aapl = pd.Series(
    [182.5, 184.1, 180.3, 185.7, 188.0,
     186.4, 190.2, 192.5, 189.8, 194.0],
    index=pd.date_range("2024-01-01", periods=10, freq="B"),
    name="AAPL_Close"
)

daily_ret  = aapl.pct_change()
total_ret  = (aapl.iloc[-1] / aapl.iloc[0] - 1) * 100
volatility = daily_ret.std() * (252 ** 0.5) * 100   # annualised
best_day   = daily_ret.idxmax()

print(f"Total return   : {total_ret:.2f}%")
print(f"Best day       : {best_day.date()}  (+{daily_ret[best_day]*100:.2f}%)")
print(f"Worst day      : {daily_ret.idxmin().date()}")
print(f"Ann. volatility: {volatility:.1f}%")
print(f"52-wk high so far: {aapl.max():.2f}")""")

RW["t3"] = rw(
"E-Commerce Product Catalog",
"<strong>Scenario:</strong> A developer loads a product catalogue to answer instant business questions: stock-outs, top-rated items, and total inventory value.",
"""\
import pandas as pd

products = pd.DataFrame({
    "sku":      ["WGT-001","GDG-042","DNT-007","WGT-002","GDG-099"],
    "name":     ["Blue Widget","Smart Gadget","Donut Maker","Red Widget","Super Gadget"],
    "category": ["Widgets","Gadgets","Kitchen","Widgets","Gadgets"],
    "price":    [29.99, 149.99, 49.99, 34.99, 199.99],
    "stock":    [120, 45, 80, 0, 23],
    "rating":   [4.5, 4.8, 3.9, 4.2, 4.7],
})

out_of_stock   = products[products["stock"] == 0][["sku","name"]]
top_rated      = products.nlargest(3, "rating")[["name","rating"]]
inventory_val  = (products["price"] * products["stock"]).sum()

print("Out of stock:\\n", out_of_stock.to_string(index=False))
print("\\nTop-rated products:\\n", top_rated.to_string(index=False))
print(f"\\nTotal inventory value: ${inventory_val:,.2f}")""")

RW["t4"] = rw(
"Loading a Messy Monthly Sales Report",
"<strong>Scenario:</strong> The finance team sends a CSV with a custom delimiter, 3 junk header rows, European date format, and an ID column that must stay as a string.",
"""\
import pandas as pd
from io import StringIO

# Simulates the messy file (semicolon-delimited, 3 junk header rows)
raw = (
    "Report generated: 2024-04-01\\n"
    "Source: CRM Export v2.3\\n"
    "\\n"
    "order_id;customer;order_date;amount;status\\n"
    "1001;Alice;01/03/2024;250.00;completed\\n"
    "1002;Bob;15/03/2024;89.50;completed\\n"
    "1003;Charlie;22/03/2024;430.75;pending\\n"
    "1004;Diana;28/03/2024;120.00;cancelled"
)

df = pd.read_csv(
    StringIO(raw),
    sep=";",
    skiprows=3,                # skip the 3 junk lines
    parse_dates=["order_date"],
    dayfirst=True,             # European DD/MM/YYYY
    dtype={"order_id": str},   # keep leading zeros
)
print(df)
print("\\nDtypes:\\n", df.dtypes)
print(f"\\nTotal revenue: ${df['amount'].sum():,.2f}")""")

RW["t5"] = rw(
"First Look at a New Customer Dataset",
"<strong>Scenario:</strong> A data scientist receives a CRM extract for a churn prediction project. They run a structured exploration before any modelling.",
"""\
import pandas as pd, numpy as np

customers = pd.DataFrame({
    "cust_id":        range(1001, 1011),
    "segment":        ["Gold","Silver","Bronze","Gold","Silver",
                       "Bronze","Gold","Silver","Bronze","Gold"],
    "age":            [34, 28, 45, np.nan, 52, 29, 38, 41, np.nan, 55],
    "monthly_spend":  [450, 120, 85, 700, 60, np.nan, 390, 200, 95, 820],
    "tenure_months":  [24, 6, 48, 36, 12, 3, 60, 18, 9, 84],
    "churned":        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
})

print(f"Shape: {customers.shape}")
print("\\nMissing values:\\n", customers.isnull().sum())
print(f"\\nChurn rate: {customers['churned'].mean()*100:.0f}%")
print("\\nSegment mix:\\n", customers["segment"].value_counts())
print("\\nNumeric summary:\\n", customers.describe().round(1))""")

RW["t6"] = rw(
"Extracting an Account Manager's Report",
"<strong>Scenario:</strong> A BI analyst pulls only Sarah's client accounts with specific columns for her weekly review, then flags contracts expiring within 3 months.",
"""\
import pandas as pd

accounts = pd.DataFrame({
    "account_id":   ["ACC001","ACC002","ACC003","ACC004","ACC005"],
    "client":       ["Acme Corp","Beta LLC","Gamma Inc","Delta Co","Epsilon Ltd"],
    "manager":      ["Sarah","John","Sarah","John","Sarah"],
    "revenue":      [45000, 32000, 78000, 12000, 56000],
    "health_score": [82, 65, 91, 44, 77],
    "contract_end": ["2025-06","2024-12","2025-03","2024-11","2025-09"],
})

# Select Sarah's accounts — specific columns only
sarahs = (
    accounts
    .loc[accounts["manager"] == "Sarah", ["client","revenue","health_score","contract_end"]]
    .sort_values("revenue", ascending=False)
    .reset_index(drop=True)
)
# iloc: pull just the revenue column as a quick sum check
sarahs["renew_soon"] = sarahs["contract_end"] <= "2025-03"

print(sarahs.to_string(index=False))
print(f"\\nTotal revenue managed: ${sarahs['revenue'].sum():,}")
print(f"Contracts expiring soon: {sarahs['renew_soon'].sum()}")""")

RW["t7"] = rw(
"Finding High-Value Customers at Churn Risk",
"<strong>Scenario:</strong> A customer-success team needs to identify Premium/Enterprise users who have been inactive for 30+ days OR gave a low NPS score, so they can intervene.",
"""\
import pandas as pd

users = pd.DataFrame({
    "user_id":        range(101, 111),
    "plan":           ["Premium","Basic","Premium","Enterprise","Basic",
                       "Premium","Basic","Enterprise","Basic","Premium"],
    "days_inactive":  [35, 5, 12, 42, 8, 60, 3, 28, 15, 7],
    "monthly_spend":  [500, 50, 520, 2100, 45, 480, 55, 1950, 48, 510],
    "nps_score":      [3, 8, 9, 2, 7, 1, 8, 4, 6, 9],
})

# Churn risk: paid plan AND (inactive 30+ days OR low NPS)
at_risk = users[
    users["plan"].isin(["Premium","Enterprise"]) &
    ((users["days_inactive"] >= 30) | (users["nps_score"] <= 3))
]

print("At-risk customers:")
print(at_risk[["user_id","plan","days_inactive","nps_score","monthly_spend"]])
print(f"\\nAt-risk monthly revenue  : ${at_risk['monthly_spend'].sum():,}")
print(f"At-risk annualised revenue: ${at_risk['monthly_spend'].sum()*12:,}")""")

RW["t8"] = rw(
"Building a Profit & Loss Report",
"<strong>Scenario:</strong> A finance analyst enriches raw sales figures with gross profit, margin %, operating profit, and YoY growth columns before exporting to the CFO.",
"""\
import pandas as pd

sales = pd.DataFrame({
    "product":      ["Widget A","Widget B","Gadget X","Gadget Y","Service Z"],
    "revenue_2024": [120000, 85000, 220000,  95000, 180000],
    "revenue_2023": [100000, 90000, 195000,  82000, 150000],
    "cogs":         [ 60000, 55000, 110000,  65000,  45000],
    "opex":         [ 20000, 15000,  40000,  20000,  25000],
})

sales["gross_profit"]     = sales["revenue_2024"] - sales["cogs"]
sales["gross_margin_pct"] = (sales["gross_profit"] / sales["revenue_2024"] * 100).round(1)
sales["operating_profit"] = sales["gross_profit"] - sales["opex"]
sales["yoy_growth_pct"]   = ((sales["revenue_2024"] - sales["revenue_2023"])
                              / sales["revenue_2023"] * 100).round(1)
sales["is_growing"]       = sales["yoy_growth_pct"] > 0

# Drop raw columns before sharing
report = sales.drop(columns=["cogs","opex","revenue_2023"])
print(report.to_string(index=False))
print(f"\\nAvg gross margin: {sales['gross_margin_pct'].mean():.1f}%")""")

RW["t9"] = rw(
"Cleaning Employee Satisfaction Survey Data",
"<strong>Scenario:</strong> HR receives a quarterly survey with many blank responses. Numeric gaps are filled with the department median; categorical gaps become 'Unknown'.",
"""\
import pandas as pd, numpy as np

survey = pd.DataFrame({
    "emp_id":          [101,102,103,104,105,106,107,108],
    "department":      ["Eng","Mkt","Eng","HR","Mkt","Eng","HR","Mkt"],
    "satisfaction":    [8, np.nan, 6, 9, np.nan, 7, np.nan, 5],
    "would_recommend": ["Yes","No",np.nan,"Yes","Yes",np.nan,"No","No"],
    "years_at_co":     [3, np.nan, 7, 1, 2, 5, np.nan, 4],
})

print("Missing before:\\n", survey.isnull().sum())

# Fill numeric with department median (fairer than global mean)
survey["satisfaction"] = (
    survey.groupby("department")["satisfaction"]
          .transform(lambda x: x.fillna(x.median()))
)
survey["years_at_co"] = survey["years_at_co"].fillna(survey["years_at_co"].median())

# Fill categorical with explicit "Unknown"
survey["would_recommend"] = survey["would_recommend"].fillna("Unknown")

print("\\nCleaned survey:\\n", survey)
print(f"\\nCompany satisfaction avg: {survey['satisfaction'].mean():.1f}/10")""")

RW["t10"] = rw(
"Fixing a Bank Transaction CSV Import",
"<strong>Scenario:</strong> A fintech developer imports a bank statement where amounts have currency symbols, dates are US-format strings, and transaction type is high-cardinality text.",
"""\
import pandas as pd
from io import StringIO

raw = (
    "date,description,amount,type\\n"
    "01/15/2024,AMAZON.COM,-$45.99,debit\\n"
    "01/16/2024,PAYROLL DEP,+$3500.00,credit\\n"
    "01/17/2024,NETFLIX,-$15.99,debit\\n"
    "01/18/2024,ATM WITHDR,-$200.00,debit\\n"
    "01/19/2024,WHOLE FOOD,-$87.30,debit"
)

df = pd.read_csv(StringIO(raw))

# Fix amount: strip $  and +, parse as float
df["amount"] = (
    df["amount"]
    .str.replace(r"[$+]", "", regex=True)
    .astype(float)
)

# Parse dates
df["date"] = pd.to_datetime(df["date"])

# Categorical for low-cardinality column (saves memory)
df["type"] = df["type"].astype("category")

# Derived columns
df["abs_amount"] = df["amount"].abs()
df["month"]      = df["date"].dt.month_name()

print(df)
print(f"\\nTotal debits : ${df[df['type']=='debit']['abs_amount'].sum():.2f}")
print(f"Total credits: ${df[df['type']=='credit']['abs_amount'].sum():.2f}")""")

RW["t11"] = rw(
"Q4 Sales Leaderboard",
"<strong>Scenario:</strong> A sales manager builds a ranked leaderboard to share at the all-hands, highlighting top performers and biggest improvers.",
"""\
import pandas as pd

reps = pd.DataFrame({
    "rep":      ["Alice","Bob","Charlie","Diana","Eve","Frank","Grace"],
    "region":   ["East","West","East","North","West","North","East"],
    "q4_deals": [42, 38, 55, 29, 47, 33, 61],
    "q4_rev":   [210000,185000,275000,140000,230000,160000,305000],
    "q3_rev":   [195000,200000,250000,130000,215000,145000,280000],
})

reps["yoy_growth"]  = ((reps["q4_rev"] - reps["q3_rev"]) / reps["q3_rev"] * 100).round(1)
reps["rank"]        = reps["q4_rev"].rank(ascending=False).astype(int)

# Leaderboard: sorted by revenue
leaderboard = reps.sort_values("q4_rev", ascending=False).reset_index(drop=True)
leaderboard.index += 1  # 1-based rank

print("=== Q4 Leaderboard ===")
print(leaderboard[["rep","region","q4_deals","q4_rev","yoy_growth"]].to_string())

print("\\n=== Top 3 Improvers ===")
print(reps.nlargest(3, "yoy_growth")[["rep","q4_rev","yoy_growth"]].to_string(index=False))""")

RW["t12"] = rw(
"Monthly Revenue Analysis by Department",
"<strong>Scenario:</strong> A business analyst produces a department-level P&L summary using named aggregations and then adds a computed profit column.",
"""\
import pandas as pd

orders = pd.DataFrame({
    "month":     ["Jan","Jan","Jan","Feb","Feb","Feb","Mar","Mar","Mar"],
    "dept":      ["Engineering","Marketing","Sales"] * 3,
    "revenue":   [45000,32000,78000, 48000,35000,82000, 51000,29000,90000],
    "cost":      [28000,18000,42000, 30000,20000,45000, 32000,16000,48000],
    "headcount": [12, 8, 15, 12, 8, 16, 13, 7, 16],
})

summary = orders.groupby("dept").agg(
    total_revenue = ("revenue",   "sum"),
    total_cost    = ("cost",      "sum"),
    avg_headcount = ("headcount", "mean"),
    months        = ("revenue",   "count"),
).round(0)

summary["gross_profit"] = summary["total_revenue"] - summary["total_cost"]
summary["margin_pct"]   = (summary["gross_profit"] / summary["total_revenue"] * 100).round(1)
summary = summary.sort_values("gross_profit", ascending=False)

print(summary.to_string())
print(f"\\nTotal company revenue: ${orders['revenue'].sum():,}")""")

RW["t13"] = rw(
"360° Customer View — Profile + Purchase History",
"<strong>Scenario:</strong> A CRM analyst joins the customer table with orders to compute CLV, average order value, and days since last purchase.",
"""\
import pandas as pd

customers = pd.DataFrame({
    "cust_id": [101,102,103,104,105],
    "name":    ["Alice","Bob","Charlie","Diana","Eve"],
    "segment": ["Gold","Silver","Bronze","Gold","Silver"],
})

orders = pd.DataFrame({
    "order_id": [1,2,3,4,5,6,7,8],
    "cust_id":  [101,102,101,103,104,101,105,102],
    "amount":   [250,180,320,90,450,280,75,220],
    "date":     pd.to_datetime(["2024-01-15","2024-01-20","2024-02-01",
                                "2024-02-10","2024-02-15","2024-03-01",
                                "2024-03-10","2024-03-15"]),
})

clv = (
    orders.groupby("cust_id")
    .agg(total_spend=("amount","sum"),
         order_count=("order_id","count"),
         last_order =("date","max"))
    .reset_index()
)

full = pd.merge(customers, clv, on="cust_id", how="left").fillna(0)
full["avg_order_value"] = (full["total_spend"] / full["order_count"].replace(0,1)).round(2)
today = pd.Timestamp("2024-03-20")
full["days_since_purchase"] = (today - full["last_order"]).dt.days

print(full[["name","segment","total_spend","order_count","avg_order_value","days_since_purchase"]])""")

RW["t14"] = rw(
"Regional Revenue Matrix for the Board Meeting",
"<strong>Scenario:</strong> A VP of Sales needs a matrix showing quarterly revenue by region with row/column totals, formatted as a one-slide PowerPoint insert.",
"""\
import pandas as pd

sales = pd.DataFrame({
    "region":  ["East","West","East","North","West","East","North","West","North"],
    "quarter": ["Q1","Q1","Q2","Q1","Q2","Q3","Q2","Q3","Q3"],
    "revenue": [120000,95000,130000,88000,105000,140000,92000,110000,98000],
})

matrix = pd.pivot_table(
    sales,
    values="revenue",
    index="region",
    columns="quarter",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="TOTAL",
)

# Format as $ thousands
fmt = matrix.applymap(lambda x: f"${x/1000:.0f}K")
print("=== Revenue by Region & Quarter ===")
print(fmt.to_string())

# Best quarter per region
best_q = matrix.drop("TOTAL").drop("TOTAL", axis=1).idxmax(axis=1)
print("\\nBest quarter per region:\\n", best_q.to_string())""")

RW["t15"] = rw(
"Standardising Messy CRM Contact Data",
"<strong>Scenario:</strong> A data engineer cleans names with random casing, emails with extra spaces, and phone numbers in mixed formats before loading into the company database.",
"""\
import pandas as pd

contacts = pd.DataFrame({
    "full_name": ["  alice johnson  ","BOB SMITH","charlie BROWN","DIANA Prince "],
    "email":     ["Alice@Gmail.COM ", " bob.smith@YAHOO.com","charlie@outlook.com","diana@corp.IO"],
    "phone":     ["(555) 123-4567","555.987.6543","555 246 8101","+1-555-369-2580"],
    "company":   ["Acme Corp.","BETA LLC","gamma inc","Delta Co"],
})

contacts["full_name"]   = contacts["full_name"].str.strip().str.title()
contacts["email"]       = contacts["email"].str.strip().str.lower()
contacts["email_domain"]= contacts["email"].str.extract(r"@([\w.]+)")[0]
contacts["phone_clean"] = contacts["phone"].str.replace(r"[^\\d]", "", regex=True)
contacts["company"]     = contacts["company"].str.strip().str.title()

# Flag non-corporate emails
corp_domains = ["gmail.com","yahoo.com","outlook.com","hotmail.com"]
contacts["is_personal_email"] = contacts["email_domain"].isin(corp_domains)

print(contacts[["full_name","email","phone_clean","email_domain","is_personal_email"]].to_string(index=False))""")

RW["t16"] = rw(
"Subscription Analytics — Tenure & Renewal Pipeline",
"<strong>Scenario:</strong> A SaaS analyst calculates customer tenure, flags subscriptions expiring in 30 days, and identifies loyal customers for a renewal discount campaign.",
"""\
import pandas as pd

today = pd.Timestamp("2025-03-01")

subs = pd.DataFrame({
    "sub_id":    ["S001","S002","S003","S004","S005"],
    "customer":  ["Acme","Beta","Gamma","Delta","Epsilon"],
    "plan":      ["Pro","Basic","Enterprise","Pro","Basic"],
    "start_date":pd.to_datetime(["2022-01-15","2024-09-01","2020-06-01","2023-03-15","2025-01-10"]),
    "end_date":  pd.to_datetime(["2025-03-15","2025-06-01","2025-02-28","2025-04-01","2026-01-10"]),
    "mrr":       [500, 99, 2000, 500, 99],
})

subs["tenure_months"]  = ((today - subs["start_date"]).dt.days / 30).astype(int)
subs["days_to_end"]    = (subs["end_date"] - today).dt.days
subs["renewing_soon"]  = subs["days_to_end"].between(0, 30)
subs["loyal"]          = subs["tenure_months"] >= 24
subs["expired"]        = subs["days_to_end"] < 0

print(subs[["customer","plan","tenure_months","days_to_end","renewing_soon","loyal"]].to_string(index=False))
print(f"\\nAt-risk MRR (renewing ≤30d): ${subs[subs['renewing_soon']]['mrr'].sum():,}")
print(f"Loyal customers: {subs['loyal'].sum()}")""")

RW["t17"] = rw(
"Tiered Discount Engine for an Order System",
"<strong>Scenario:</strong> An e-commerce backend applies tiered discounts: >$500 = 15%, $200-$500 = 10%, <$200 = 5%. VIP customers get an extra 5% on top.",
"""\
import pandas as pd, numpy as np

orders = pd.DataFrame({
    "order_id": [1001,1002,1003,1004,1005,1006],
    "customer": ["Alice","Bob","Charlie","Diana","Eve","Frank"],
    "subtotal": [650.00, 320.00, 95.00, 1200.00, 185.00, 480.00],
    "vip":      [True, False, False, True, False, True],
})

def discount_rate(row):
    base = 0.15 if row["subtotal"] >= 500 else (0.10 if row["subtotal"] >= 200 else 0.05)
    return base + (0.05 if row["vip"] else 0.0)

orders["discount_pct"] = orders.apply(discount_rate, axis=1)
orders["discount_amt"] = (orders["subtotal"] * orders["discount_pct"]).round(2)
orders["final_price"]  = (orders["subtotal"] - orders["discount_amt"]).round(2)

# Vectorised alternative using np.where (faster for large DataFrames)
orders["tier"] = np.where(orders["subtotal"] >= 500, "Premium",
                 np.where(orders["subtotal"] >= 200, "Standard", "Basic"))

print(orders[["order_id","customer","subtotal","discount_pct","discount_amt","final_price","tier"]].to_string(index=False))
print(f"\\nTotal discounts given: ${orders['discount_amt'].sum():.2f}")""")

RW["t18"] = rw(
"Reshaping Survey Data for a Heatmap",
"<strong>Scenario:</strong> A UX researcher melts wide-format feature-ratings into long format for seaborn, then pivots back to a per-feature summary.",
"""\
import pandas as pd

# Wide: each row = respondent, each column = feature score
survey = pd.DataFrame({
    "user_id":      [101,102,103,104,105],
    "checkout_flow":[4, 5, 3, 4, 5],
    "search_bar":   [3, 4, 5, 2, 3],
    "mobile_app":   [5, 5, 4, 5, 4],
    "payment_page": [2, 3, 2, 4, 3],
    "help_center":  [4, 2, 3, 3, 5],
})

# Melt to long (required by seaborn / most viz libraries)
long = pd.melt(survey, id_vars=["user_id"],
               var_name="feature", value_name="rating")
print("Long format (first 6 rows):")
print(long.head(6))

# Per-feature averages
avg = long.groupby("feature")["rating"].agg(["mean","count","std"]).round(2)
avg = avg.sort_values("mean", ascending=False)
print("\\nFeature ratings (ranked):")
print(avg)

# Back to wide for the heatmap matrix
heatmap_data = long.pivot(index="feature", columns="user_id", values="rating")
print("\\nHeatmap matrix shape:", heatmap_data.shape)""")

RW["t19"] = rw(
"A/B Test Analysis for a Landing Page",
"<strong>Scenario:</strong> A growth team ran a landing page A/B test. They analyse conversion rates, compute lift, and check correlations to decide which variant wins.",
"""\
import pandas as pd, numpy as np

np.random.seed(42)
n = 500  # visitors per variant

ab = pd.DataFrame({
    "variant":     ["A"] * n + ["B"] * n,
    "converted":   np.concatenate([
                       np.random.binomial(1, 0.12, n),   # A: 12% CVR
                       np.random.binomial(1, 0.155, n),  # B: 15.5% CVR
                   ]),
    "time_on_page":np.concatenate([
                       np.random.normal(45, 15, n),
                       np.random.normal(52, 18, n),
                   ]).round(1),
})

summary = ab.groupby("variant").agg(
    visitors    = ("converted", "count"),
    conversions = ("converted", "sum"),
    cvr_pct     = ("converted", lambda x: round(x.mean()*100, 2)),
    avg_time_s  = ("time_on_page", "mean"),
).round(2)

print(summary)

cvr_a = summary.loc["A","cvr_pct"]
cvr_b = summary.loc["B","cvr_pct"]
lift  = (cvr_b - cvr_a) / cvr_a * 100
print(f"\\nLift (B vs A): +{lift:.1f}%")
print(f"Revenue impact (1M visitors, $50 AOV): ${1e6 * (cvr_b-cvr_a)/100 * 50:,.0f}")
print(f"Time→convert corr: {ab['time_on_page'].corr(ab['converted']):.3f}")""")

RW["t20"] = rw(
"6-Month Revenue Dashboard",
"<strong>Scenario:</strong> A data analyst builds a 3-panel matplotlib dashboard — revenue vs target, mix by category, and MoM growth — for the company all-hands.",
"""\
import pandas as pd
import matplotlib.pyplot as plt

monthly = pd.DataFrame({
    "Month":    pd.date_range("2024-01", periods=6, freq="ME"),
    "Revenue":  [185000,210000,195000,240000,228000,265000],
    "Target":   [200000,200000,200000,220000,220000,250000],
    "SaaS":     [ 80000, 95000, 88000,110000,105000,125000],
    "Services": [ 70000, 80000, 75000, 90000, 85000, 95000],
    "Hardware": [ 35000, 35000, 32000, 40000, 38000, 45000],
})

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
fig.suptitle("H1 2024 Revenue Dashboard", fontsize=14, fontweight="bold")

monthly.set_index("Month")[["Revenue","Target"]].plot(
    ax=axes[0], marker="o", title="Revenue vs Target")

monthly.set_index("Month")[["SaaS","Services","Hardware"]].plot(
    kind="bar", stacked=True, ax=axes[1], title="Revenue Mix")
axes[1].set_xticklabels([d.strftime("%b") for d in monthly["Month"]], rotation=30)

monthly["MoM"] = monthly["Revenue"].pct_change() * 100
colors = ["#2ecc71" if x > 0 else "#e74c3c" for x in monthly["MoM"].fillna(0)]
monthly.set_index("Month")["MoM"].plot(kind="bar", ax=axes[2], color=colors, title="MoM Growth %")

plt.tight_layout()
plt.savefig("revenue_dashboard.png", dpi=100, bbox_inches="tight")
plt.show()
print("Dashboard saved.")""")

RW["t21"] = rw(
"Deduplicating a CRM Customer Export",
"<strong>Scenario:</strong> A data-ops team merges two CRM systems and finds duplicate customers caused by the migration. They keep the most recently updated record per email address.",
"""\
import pandas as pd

crm = pd.DataFrame({
    "email":        ["alice@co.com","bob@co.com","alice@co.com","charlie@co.com","bob@co.com"],
    "name":         ["Alice Smith","Bob Jones","Alice Smith","Charlie Brown","Bob Jones"],
    "plan":         ["Pro","Basic","Pro","Enterprise","Pro"],  # plan changed in v2!
    "last_updated": ["2024-03-01","2024-01-15","2024-03-20","2024-02-10","2024-03-18"],
    "source":       ["CRM_v1","CRM_v1","CRM_v2","CRM_v1","CRM_v2"],
})

print(f"Before: {len(crm)} rows, {crm['email'].nunique()} unique customers")
print(f"Duplicated emails: {crm.duplicated(subset=['email']).sum()}")

# Sort by date so latest is last, then keep last per email
crm_clean = (
    crm
    .sort_values("last_updated")
    .drop_duplicates(subset=["email"], keep="last")
    .reset_index(drop=True)
)

print(f"\\nAfter: {len(crm_clean)} rows")
print(crm_clean[["email","name","plan","last_updated","source"]].to_string(index=False))""")

RW["t22"] = rw(
"Customer Lifetime Value (CLV) Segmentation",
"<strong>Scenario:</strong> A marketing analyst segments customers into spend tiers for campaign targeting: Low → re-engagement email, Mid → upsell offer, High → VIP white-glove treatment.",
"""\
import pandas as pd

customers = pd.DataFrame({
    "customer_id": range(1001, 1011),
    "total_spent": [1250, 320, 4500, 89, 780, 2100, 560, 3800, 150, 920],
    "age":         [34, 52, 28, 19, 45, 37, 61, 29, 24, 42],
})

# CLV tier by spend (equal-width bins)
customers["clv_tier"] = pd.cut(
    customers["total_spent"],
    bins=[0, 500, 1500, 5000],
    labels=["Low", "Mid", "High"],
)

# Age group by quantile (equal-frequency — same number per bucket)
customers["age_group"] = pd.qcut(
    customers["age"], q=3,
    labels=["18-30", "31-45", "46+"],
)

# Revenue share per tier
tier_stats = customers.groupby("clv_tier", observed=True).agg(
    count     = ("customer_id", "count"),
    avg_spend = ("total_spent",  "mean"),
    pct_rev   = ("total_spent",  lambda x: x.sum() / customers["total_spent"].sum() * 100),
).round(1)

print(customers[["customer_id","total_spent","clv_tier","age_group"]])
print("\\nTier revenue breakdown:")
print(tier_stats)""")

RW["t23"] = rw(
"Reusable ETL Pipeline for Raw Sales Data",
"<strong>Scenario:</strong> A data engineer builds a composable, readable pipeline using pipe() that takes messy raw order exports and produces clean analysis-ready DataFrames.",
"""\
import pandas as pd, numpy as np

raw = pd.DataFrame({
    "order_id": ["ORD-001","ORD-002","ORD-003","ORD-004","ORD-005"],
    "customer": ["  alice  ","BOB","charlie","  DIANA  ","eve"],
    "amount":   [250.0, -99.0, 430.0, np.nan, 185.0],
    "quantity": [2, 1, 3, 1, 2],
    "date":     ["2024-01-15","2024-01-16","2024-01-16","2024-01-17","2024-01-18"],
    "status":   ["completed","cancelled","completed","pending","completed"],
})

# Composable pipeline functions
def clean_strings(df):
    df = df.copy()
    df["customer"] = df["customer"].str.strip().str.title()
    return df

def remove_bad_orders(df):
    return df[(df["amount"] > 0) & df["amount"].notna()]

def enrich(df):
    return df.assign(
        date        = pd.to_datetime(df["date"]),
        revenue     = df["amount"] * df["quantity"],
        day_of_week = lambda x: x["date"].dt.day_name(),
        is_weekend  = lambda x: x["date"].dt.dayofweek >= 5,
    )

# Chain everything with .pipe()
clean = (
    raw
    .pipe(clean_strings)
    .pipe(remove_bad_orders)
    .pipe(enrich)
    .query("status == 'completed'")
    .sort_values("revenue", ascending=False)
    .reset_index(drop=True)
)

print(clean[["order_id","customer","amount","quantity","revenue","day_of_week"]])""")

RW["t24"] = rw(
"Fast Financial Ratio Calculations",
"<strong>Scenario:</strong> A financial analyst computes multiple P&L ratios across 1,000 companies. eval() is faster than chained column assignments and keeps the code readable.",
"""\
import pandas as pd, numpy as np

np.random.seed(0)
n = 1000
fin = pd.DataFrame({
    "company": [f"CO_{i:04d}" for i in range(n)],
    "revenue":    np.random.uniform(1e6, 100e6, n),
    "cogs_pct":   np.random.uniform(0.30, 0.65, n),
    "opex_pct":   np.random.uniform(0.10, 0.25, n),
    "interest_pct": np.random.uniform(0.01, 0.05, n),
    "tax_rate":   np.random.uniform(0.20, 0.30, n),
})

# Build P&L with eval (compiles to fast bytecode)
fin.eval("cogs           = revenue * cogs_pct",       inplace=True)
fin.eval("gross_profit   = revenue - cogs",           inplace=True)
fin.eval("opex           = revenue * opex_pct",       inplace=True)
fin.eval("ebit           = gross_profit - opex",      inplace=True)
fin.eval("interest_exp   = revenue * interest_pct",   inplace=True)
fin.eval("ebt            = ebit - interest_exp",      inplace=True)
fin.eval("net_income     = ebt * (1 - tax_rate)",     inplace=True)
fin.eval("gross_margin   = gross_profit / revenue",   inplace=True)
fin.eval("net_margin     = net_income   / revenue",   inplace=True)

# Filter: profitable companies with gross margin > 50%
profitable = fin.query("net_income > 0 and gross_margin > 0.50")
print(f"Profitable high-margin companies: {len(profitable)}/{n}")
print(profitable[["company","revenue","gross_margin","net_margin"]].nlargest(5,"net_margin").round(3).to_string(index=False))""")

RW["t25"] = rw(
"Multi-Store Quarterly Inventory Report",
"<strong>Scenario:</strong> A retail chain analyst uses MultiIndex to track inventory across 3 stores and 4 quarters, enabling instant cross-sectional slicing.",
"""\
import pandas as pd, numpy as np

stores   = ["NYC", "LA", "Chicago"]
quarters = ["Q1", "Q2", "Q3", "Q4"]
idx = pd.MultiIndex.from_product([stores, quarters], names=["store","quarter"])

np.random.seed(0)
inv = pd.DataFrame({
    "units_sold":   np.random.randint(200, 800, len(idx)),
    "units_ordered":np.random.randint(300, 700, len(idx)),
    "revenue":      np.random.randint(10000, 60000, len(idx)),
}, index=idx)

inv["net_stock"] = inv["units_ordered"] - inv["units_sold"]

print("=== NYC performance all quarters ===")
print(inv.loc["NYC"])

print("\\n=== All stores, Q4 only ===")
print(inv.xs("Q4", level="quarter"))

print("\\n=== Annual revenue per store ===")
print(inv.groupby(level="store")["revenue"].sum().sort_values(ascending=False))

print("\\n=== Revenue matrix (stores × quarters) ===")
print(inv["revenue"].unstack(level="quarter"))""")

RW["t26"] = rw(
"NPS Survey Analysis with Ordered Ratings",
"<strong>Scenario:</strong> A product team classifies 0–10 NPS responses into Detractor/Passive/Promoter ordered categories so they sort and group correctly, and empty categories still appear.",
"""\
import pandas as pd

survey = pd.DataFrame({
    "respondent": range(1, 11),
    "product":    ["App","App","Web","App","Web","App","Web","App","Web","Web"],
    "nps_score":  [9, 6, 8, 10, 4, 7, 9, 3, 8, 6],
    "plan":       ["Pro","Basic","Pro","Enterprise","Basic",
                   "Pro","Basic","Pro","Enterprise","Basic"],
})

def nps_label(score):
    return "Promoter" if score >= 9 else ("Passive" if score >= 7 else "Detractor")

survey["nps_cat"] = pd.Categorical(
    survey["nps_score"].apply(nps_label),
    categories=["Detractor","Passive","Promoter"],
    ordered=True,
)

# groupby with observed=False shows all categories even if empty
breakdown = survey.groupby("nps_cat", observed=False).agg(
    count     = ("respondent", "count"),
    avg_score = ("nps_score", "mean"),
).round(2)

n = len(survey)
breakdown["pct"] = (breakdown["count"] / n * 100).round(1)

nps_idx = breakdown.loc["Promoter","pct"] - breakdown.loc["Detractor","pct"]
print(breakdown)
print(f"\\nNPS Index: {nps_idx:.0f}  (range -100 to +100)")
print("\\nSorts correctly by category order:")
print(survey.sort_values("nps_cat")[["respondent","nps_score","nps_cat"]].to_string(index=False))""")

RW["t27"] = rw(
"Stock Technical Analysis — SMA, EMA & Bollinger Bands",
"<strong>Scenario:</strong> A quant analyst computes SMA-20, EMA-12, MACD, and Bollinger Bands to generate buy/sell signals on a simulated stock.",
"""\
import pandas as pd, numpy as np

np.random.seed(42)
n = 60
price = pd.Series(
    100 + np.cumsum(np.random.normal(0.2, 2.0, n)),
    index=pd.date_range("2024-01-01", periods=n, freq="B"),
    name="Close",
)

ta = pd.DataFrame({"Close": price})

# Simple & Exponential Moving Averages
ta["SMA_20"]    = price.rolling(20).mean()
ta["EMA_12"]    = price.ewm(span=12).mean()
ta["EMA_26"]    = price.ewm(span=26).mean()

# MACD indicator
ta["MACD"]      = ta["EMA_12"] - ta["EMA_26"]
ta["Signal"]    = ta["MACD"].ewm(span=9).mean()
ta["Histogram"] = ta["MACD"] - ta["Signal"]

# Bollinger Bands (2 standard deviations)
rolling_std      = price.rolling(20).std()
ta["BB_upper"]   = ta["SMA_20"] + 2 * rolling_std
ta["BB_lower"]   = ta["SMA_20"] - 2 * rolling_std

# Expanding all-time-high
ta["ATH"]        = price.expanding().max()

# Buy signal: price below lower Bollinger Band
ta["buy_signal"] = price < ta["BB_lower"]

print(ta.tail(10).round(2))
print(f"\\nBuy signals triggered: {ta['buy_signal'].sum()} days")""")

RW["t28"] = rw(
"Color-Coded Weekly KPI Report for Management",
"<strong>Scenario:</strong> A BI analyst creates a styled HTML table with conditional formatting — green/red cells and data bars — for the weekly business review.",
"""\
import pandas as pd

kpis = pd.DataFrame({
    "Metric":      ["Revenue","New Customers","Churn Rate","NPS","Avg Order Value","Support CSAT"],
    "This Week":   [285000, 142, 2.1, 48, 210, 91],
    "Last Week":   [262000, 128, 2.8, 44, 198, 88],
    "Target":      [275000, 150, 2.0, 50, 205, 90],
})

kpis["vs Target %"] = ((kpis["This Week"] - kpis["Target"]) / kpis["Target"] * 100).round(1)
kpis["WoW %"]       = ((kpis["This Week"] - kpis["Last Week"]) / kpis["Last Week"] * 100).round(1)

styled = (
    kpis.style
    .format({"This Week": "{:,.0f}", "Last Week": "{:,.0f}",
             "Target":    "{:,.0f}", "vs Target %": "{:+.1f}%", "WoW %": "{:+.1f}%"})
    .background_gradient(subset=["vs Target %"], cmap="RdYlGn", vmin=-10, vmax=10)
    .background_gradient(subset=["WoW %"],       cmap="RdYlGn", vmin=-10, vmax=10)
    .bar(subset=["This Week"], color="#4a90d9")
    .set_caption("Weekly KPIs — w/e 7 Mar 2025")
    .hide(axis="index")
)

# In Jupyter, `styled` renders the HTML table. Here we print insights:
print(kpis[["Metric","This Week","Target","vs Target %"]].to_string(index=False))
# Export to HTML for email
html_table = styled.to_html()
with open("weekly_kpis.html", "w") as f:
    f.write(html_table)
print("\\nHTML table saved to weekly_kpis.html")""")

RW["t29"] = rw(
"Optimising a 500K-Row Transaction Log",
"<strong>Scenario:</strong> A data engineer processes a large e-commerce transaction log that is consuming too much RAM. Type downcast + categorical columns reduce memory by ~75%.",
"""\
import pandas as pd, numpy as np

np.random.seed(0)
n = 500_000

txn = pd.DataFrame({
    "txn_id":     np.arange(n),
    "user_id":    np.random.randint(1, 100_000, n),
    "product_id": np.random.randint(1, 10_000,  n),
    "category":   np.random.choice(["Electronics","Clothing","Books","Food","Sports"], n),
    "country":    np.random.choice(["US","UK","CA","AU","DE"], n),
    "amount":     np.random.uniform(1.0, 500.0, n),
    "quantity":   np.random.randint(1, 10, n),
    "returned":   np.random.randint(0, 2, n),
})

before_mb = txn.memory_usage(deep=True).sum() / 1e6
print(f"Before: {before_mb:.1f} MB  |  dtypes: {txn.dtypes.value_counts().to_dict()}")

# Downcast integers
txn["txn_id"]     = txn["txn_id"].astype("uint32")
txn["user_id"]    = txn["user_id"].astype("uint32")
txn["product_id"] = txn["product_id"].astype("uint16")
txn["quantity"]   = txn["quantity"].astype("int8")
txn["returned"]   = txn["returned"].astype("int8")

# Float32 instead of float64
txn["amount"]     = txn["amount"].astype("float32")

# Categorical for low-cardinality strings (5 unique values each!)
txn["category"]   = txn["category"].astype("category")
txn["country"]    = txn["country"].astype("category")

after_mb = txn.memory_usage(deep=True).sum() / 1e6
print(f"After:  {after_mb:.1f} MB")
print(f"Saved:  {(1 - after_mb/before_mb)*100:.0f}%  ✓")""")

RW["t30"] = rw(
"Stratified Train / Validation / Test Split for a Churn Model",
"<strong>Scenario:</strong> A ML engineer needs reproducible train/val/test splits that preserve the 20% churn rate (class imbalance) in every split.",
"""\
import pandas as pd, numpy as np

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    "cust_id":     range(1, n+1),
    "tenure":      np.random.randint(1, 72, n),
    "spend":       np.random.uniform(20, 500, n).round(2),
    "calls":       np.random.randint(0, 15, n),
    "churn":       np.random.choice([0, 1], n, p=[0.80, 0.20]),
})

print(f"Full dataset  churn rate: {df['churn'].mean():.1%}  ({n} rows)")

def stratified_split(df, label, train=0.70, val=0.15, seed=42):
    tr = df.groupby(label, group_keys=False).apply(
             lambda x: x.sample(frac=train, random_state=seed))
    rem = df.drop(tr.index)
    va  = rem.groupby(label, group_keys=False).apply(
              lambda x: x.sample(frac=val/(1-train), random_state=seed))
    te  = rem.drop(va.index)
    return tr.reset_index(drop=True), va.reset_index(drop=True), te.reset_index(drop=True)

train, val, test = stratified_split(df, "churn")

for name, split in [("Train", train), ("Val", val), ("Test", test)]:
    print(f"{name:5s}  rows={len(split):4d}  churn={split['churn'].mean():.1%}")""")

RW["t31"] = rw(
"Portfolio Daily Returns & Drawdown Analysis",
"<strong>Scenario:</strong> A portfolio manager calculates daily log-returns, cumulative NAV growth, maximum drawdown, and annualised Sharpe ratio.",
"""\
import pandas as pd, numpy as np

np.random.seed(1)
nav = pd.Series(
    [10000] + list(10000 * np.cumprod(1 + np.random.normal(0.0005, 0.015, 59))),
    index=pd.date_range("2024-01-02", periods=60, freq="B"),
    name="NAV",
)

pf = pd.DataFrame({"NAV": nav})

pf["daily_return"]  = pf["NAV"].pct_change()
pf["log_return"]    = np.log(pf["NAV"] / pf["NAV"].shift(1))
pf["cum_return_pct"]= (pf["NAV"] / pf["NAV"].iloc[0] - 1) * 100
pf["rolling_max"]   = pf["NAV"].expanding().max()
pf["drawdown_pct"]  = (pf["NAV"] - pf["rolling_max"]) / pf["rolling_max"] * 100
pf["vol_10d_ann"]   = pf["daily_return"].rolling(10).std() * np.sqrt(252) * 100

max_dd  = pf["drawdown_pct"].min()
total_r = pf["cum_return_pct"].iloc[-1]
sharpe  = (pf["daily_return"].mean() / pf["daily_return"].std()) * np.sqrt(252)

print(pf[["NAV","daily_return","cum_return_pct","drawdown_pct"]].tail(10).round(3).to_string())
print(f"\\nTotal return : {total_r:+.2f}%")
print(f"Max drawdown : {max_dd:.2f}%")
print(f"Sharpe ratio : {sharpe:.2f}")""")

RW["t32"] = rw(
"E-Commerce: Expand Cart Items for Co-Purchase Analysis",
"<strong>Scenario:</strong> An analyst needs to find the most frequently purchased products. Raw orders store items as lists — explode() unpacks them for item-level analysis.",
"""\
import pandas as pd

orders = pd.DataFrame({
    "order_id":    [5001, 5002, 5003, 5004, 5005],
    "customer":    ["Alice","Bob","Alice","Charlie","Bob"],
    "items":       [["USB-Hub","Webcam","Mouse"],
                    ["Keyboard","Mouse"],
                    ["Monitor","USB-Hub","Webcam","Headphones"],
                    ["Mouse","Keyboard","USB-Hub"],
                    ["Webcam","Headphones"]],
    "order_value": [89.50, 125.00, 349.99, 210.00, 75.50],
})

# Explode: one row per item (order_value is repeated per item)
items = orders.explode("items").rename(columns={"items":"product"}).reset_index(drop=True)

print("Exploded (first 8 rows):")
print(items.head(8))

print("\\nTop products by frequency:")
print(items["product"].value_counts())

# Co-purchase: how often does Webcam appear with Mouse?
webcam_orders = items[items["product"]=="Webcam"]["order_id"]
print("\\nProducts bought with Webcam:")
print(items[items["order_id"].isin(webcam_orders)]["product"].value_counts())""")

RW["cheatsheet"] = rw(
"End-to-End Data Pipeline in 30 Lines",
"<strong>Scenario:</strong> A data analyst takes raw data from ingestion to a final analytical summary — combining all major pandas techniques in one concise workflow.",
"""\
import pandas as pd, numpy as np
from io import StringIO

# 1. Simulate raw CSV data (replace with pd.read_csv("sales.csv") in real life)
raw = StringIO(
    "order_id,customer,date,amount,product,region\\n"
    "001,Alice,2024-01-10,250,Widget A,East\\n"
    "002,Bob,2024-01-15,180,Gadget X,West\\n"
    "002,Bob,2024-01-15,180,Gadget X,West\\n"     # duplicate!
    "003,Charlie,2024-02-01,430,Widget B,East\\n"
    "004,Diana,2024-02-20,,Service Z,North\\n"    # missing amount
    "005,Alice,2024-03-05,520,Widget A,East\\n"
)

# 2. Load
df = pd.read_csv(raw, dtype={"order_id": str}, parse_dates=["date"])

# 3. Clean
df = (df
      .dropna(subset=["amount"])
      .drop_duplicates(subset=["order_id"])
      .assign(customer=lambda x: x["customer"].str.title()))

# 4. Enrich
df = df.assign(
    month      = df["date"].dt.to_period("M").astype(str),
    quarter    = "Q" + df["date"].dt.quarter.astype(str),
    revenue_k  = (df["amount"] / 1000).round(2),
    value_band = pd.cut(df["amount"], bins=[0,200,400,9999], labels=["Low","Mid","High"]),
)

# 5. Analyse
summary = df.groupby(["region","quarter"]).agg(
    orders     = ("order_id", "count"),
    total_rev  = ("amount",   "sum"),
    avg_order  = ("amount",   "mean"),
).round(1)
print(summary)

# 6. Save
df.to_csv("clean_sales.csv", index=False)
print(f"\\nClean data saved ({len(df)} orders).")""")

# ── Inject into HTML ──────────────────────────────────────────────────────────
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

def find_topic_body_end(html, topic_id):
    """Return the index of the closing </div> for topic-body of the given topic."""
    start = html.find(f'<div class="topic" id="{topic_id}">')
    if start == -1:
        return -1
    body_start = html.find('<div class="topic-body">', start)
    if body_start == -1:
        return -1
    depth = 0
    pos   = body_start
    while pos < len(html):
        open_pos  = html.find("<div",   pos)
        close_pos = html.find("</div>", pos)
        if close_pos == -1:
            break
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            pos = open_pos + 4
        else:
            depth -= 1
            if depth == 0:
                return close_pos
            pos = close_pos + 6
    return -1

count = 0
for tid, content in RW.items():
    idx = find_topic_body_end(html, tid)
    if idx == -1:
        print(f"  WARNING: topic '{tid}' not found — skipped")
        continue
    html = html[:idx] + content + "\n    " + html[idx:]
    count += 1
    print(f"  Injected: {tid}")

# Add CSS for the new blocks
CSS = """
  /* ── Real-World Use Case Blocks ──────────────────────────────── */
  .rw-block { border-top: 2px solid rgba(63,185,80,.18); }
  .rw-header {
    padding: 9px 20px 8px;
    font-size: 11.5px; font-weight: 700; letter-spacing:.04em;
    color: var(--accent2);
    background: rgba(63,185,80,.07);
    border-bottom: 1px solid rgba(63,185,80,.18);
  }
  .rw-desc {
    padding: 10px 20px 12px;
    font-size: 13px; color: var(--text-muted); line-height: 1.65;
    border-bottom: 1px solid var(--border);
  }
  .rw-desc strong { color: var(--text); }
"""
html = html.replace("  /* ── Scrollbar", CSS + "\n  /* ── Scrollbar", 1)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nHTML updated — {count} topics injected.")

# ── Append real-world cells to notebook ──────────────────────────────────────
with open(NB_FILE, encoding="utf-8") as f:
    nb = json.load(f)

NB_RW = [
    nb_md("---\n## Real-World Use Cases (one per topic)\nEach cell below mirrors the real-world example in `index.html` so you can run them interactively.", "rw-intro"),

    nb_md("### 01 · Setting Up a Project Environment", "rw-01-md"),
    nb_code("""\
import pandas as pd, numpy as np, matplotlib.pyplot as plt
pd.set_option("display.max_columns", 50)
pd.set_option("display.float_format", "{:,.2f}".format)
print(f"pandas {pd.__version__}  |  numpy {np.__version__}")""", "rw-01"),

    nb_md("### 02 · Stock Price Tracker", "rw-02-md"),
    nb_code("""\
aapl = pd.Series([182.5,184.1,180.3,185.7,188.0,186.4,190.2,192.5,189.8,194.0],
    index=pd.date_range("2024-01-01", periods=10, freq="B"), name="AAPL")
ret = aapl.pct_change()
print(f"Total return   : {(aapl.iloc[-1]/aapl.iloc[0]-1)*100:.2f}%")
print(f"Best day       : {ret.idxmax().date()}  (+{ret.max()*100:.2f}%)")
print(f"Ann. volatility: {ret.std()*(252**0.5)*100:.1f}%")""", "rw-02"),

    nb_md("### 03 · E-Commerce Product Catalog", "rw-03-md"),
    nb_code("""\
products = pd.DataFrame({
    "sku":      ["WGT-001","GDG-042","DNT-007","WGT-002","GDG-099"],
    "name":     ["Blue Widget","Smart Gadget","Donut Maker","Red Widget","Super Gadget"],
    "price":    [29.99, 149.99, 49.99, 34.99, 199.99],
    "stock":    [120, 45, 80, 0, 23],
    "rating":   [4.5, 4.8, 3.9, 4.2, 4.7],
})
print("Out of stock:\\n", products[products["stock"]==0][["sku","name"]].to_string(index=False))
print(f"Inventory value: ${(products['price']*products['stock']).sum():,.2f}")""", "rw-03"),

    nb_md("### 04 · Loading a Messy Sales CSV", "rw-04-md"),
    nb_code("""\
from io import StringIO
raw = ("order_id;customer;order_date;amount;status\\n"
       "1001;Alice;01/03/2024;250.00;completed\\n"
       "1002;Bob;15/03/2024;89.50;completed\\n"
       "1003;Charlie;22/03/2024;430.75;pending")
df = pd.read_csv(StringIO(raw), sep=";",
                 parse_dates=["order_date"], dayfirst=True,
                 dtype={"order_id": str})
print(df)""", "rw-04"),

    nb_md("### 05 · First-Look at a New Dataset", "rw-05-md"),
    nb_code("""\
cust = pd.DataFrame({
    "segment":       ["Gold","Silver","Bronze","Gold","Silver"],
    "monthly_spend": [450, 120, 85, 700, 60],
    "churned":       [0, 0, 1, 0, 1],
})
print(cust.describe())
print("\\nChurn rate:", cust["churned"].mean()*100, "%")""", "rw-05"),

    nb_md("### 06 · Account Manager Report (loc / iloc)", "rw-06-md"),
    nb_code("""\
accounts = pd.DataFrame({
    "client":   ["Acme","Beta","Gamma","Delta","Epsilon"],
    "manager":  ["Sarah","John","Sarah","John","Sarah"],
    "revenue":  [45000, 32000, 78000, 12000, 56000],
    "contract_end": ["2025-06","2024-12","2025-03","2024-11","2025-09"],
})
sarah = accounts.loc[accounts["manager"]=="Sarah", ["client","revenue","contract_end"]]
print(sarah.sort_values("revenue", ascending=False).to_string(index=False))""", "rw-06"),

    nb_md("### 07 · Churn-Risk Customers (Filtering)", "rw-07-md"),
    nb_code("""\
users = pd.DataFrame({
    "user_id": range(101,111),
    "plan": ["Premium","Basic","Premium","Enterprise","Basic","Premium","Basic","Enterprise","Basic","Premium"],
    "days_inactive": [35,5,12,42,8,60,3,28,15,7],
    "nps_score":     [3,8,9,2,7,1,8,4,6,9],
    "monthly_spend": [500,50,520,2100,45,480,55,1950,48,510],
})
at_risk = users[users["plan"].isin(["Premium","Enterprise"]) &
                ((users["days_inactive"]>=30)|(users["nps_score"]<=3))]
print(at_risk[["user_id","plan","days_inactive","nps_score","monthly_spend"]])
print(f"At-risk ARR: ${at_risk['monthly_spend'].sum()*12:,}")""", "rw-07"),

    nb_md("### 08 · P&L Report (Adding Columns)", "rw-08-md"),
    nb_code("""\
pnl = pd.DataFrame({
    "product": ["Widget A","Widget B","Gadget X"],
    "revenue": [120000, 85000, 220000],
    "cogs":    [ 60000, 55000, 110000],
    "opex":    [ 20000, 15000,  40000],
})
pnl["gross_profit"]    = pnl["revenue"] - pnl["cogs"]
pnl["gross_margin_%"]  = (pnl["gross_profit"]/pnl["revenue"]*100).round(1)
pnl["operating_profit"]= pnl["gross_profit"] - pnl["opex"]
print(pnl.to_string(index=False))""", "rw-08"),

    nb_md("### 09 · Cleaning Survey Missing Data", "rw-09-md"),
    nb_code("""\
import numpy as np
survey = pd.DataFrame({
    "department":     ["Eng","Mkt","Eng","HR","Mkt"],
    "satisfaction":   [8, np.nan, 6, 9, np.nan],
    "recommend":      ["Yes","No",None,"Yes","Yes"],
})
survey["satisfaction"] = survey.groupby("department")["satisfaction"].transform(
    lambda x: x.fillna(x.median()))
survey["recommend"] = survey["recommend"].fillna("Unknown")
print(survey)""", "rw-09"),

    nb_md("### 10 · Fixing Bank Transaction Types", "rw-10-md"),
    nb_code("""\
from io import StringIO
raw = ("date,description,amount,type\\n"
       "01/15/2024,AMAZON,-$45.99,debit\\n"
       "01/16/2024,PAYROLL,+$3500.00,credit\\n"
       "01/17/2024,NETFLIX,-$15.99,debit")
df = pd.read_csv(StringIO(raw))
df["amount"] = df["amount"].str.replace(r"[$+]","",regex=True).astype(float)
df["date"]   = pd.to_datetime(df["date"])
df["type"]   = df["type"].astype("category")
print(df)""", "rw-10"),

    nb_md("### 11 · Sales Leaderboard (Sorting)", "rw-11-md"),
    nb_code("""\
reps = pd.DataFrame({
    "rep":    ["Alice","Bob","Charlie","Diana","Eve"],
    "q4_rev": [210000,185000,275000,140000,305000],
    "q3_rev": [195000,200000,250000,130000,280000],
})
reps["growth_%"] = ((reps["q4_rev"]-reps["q3_rev"])/reps["q3_rev"]*100).round(1)
print("=== Leaderboard ===")
print(reps.sort_values("q4_rev", ascending=False).to_string(index=False))
print("\\n=== Top Growers ===")
print(reps.nlargest(3,"growth_%")[["rep","growth_%"]].to_string(index=False))""", "rw-11"),

    nb_md("### 12 · Monthly Revenue by Department (GroupBy)", "rw-12-md"),
    nb_code("""\
orders = pd.DataFrame({
    "dept":    ["Eng","Mkt","Sales"]*3,
    "revenue": [45000,32000,78000,48000,35000,82000,51000,29000,90000],
    "cost":    [28000,18000,42000,30000,20000,45000,32000,16000,48000],
})
summary = orders.groupby("dept").agg(
    total_rev=("revenue","sum"), total_cost=("cost","sum")).eval("margin=total_rev-total_cost")
print(summary.sort_values("margin", ascending=False))""", "rw-12"),

    nb_md("### 13 · Customer 360° View (Merge)", "rw-13-md"),
    nb_code("""\
customers = pd.DataFrame({"cust_id":[101,102,103],"name":["Alice","Bob","Charlie"],"segment":["Gold","Silver","Bronze"]})
orders = pd.DataFrame({"order_id":[1,2,3,4,5],"cust_id":[101,102,101,103,102],"amount":[250,180,320,90,220]})
clv = orders.groupby("cust_id").agg(total=("amount","sum"),count=("order_id","count")).reset_index()
full = pd.merge(customers, clv, on="cust_id", how="left").fillna(0)
full["avg_order"] = (full["total"]/full["count"].replace(0,1)).round(2)
print(full.to_string(index=False))""", "rw-13"),

    nb_md("### 14 · Regional Sales Matrix (Pivot Table)", "rw-14-md"),
    nb_code("""\
sales = pd.DataFrame({
    "region":  ["East","West","North","East","West","North"],
    "quarter": ["Q1","Q1","Q1","Q2","Q2","Q2"],
    "revenue": [120000,95000,88000,130000,105000,92000],
})
matrix = pd.pivot_table(sales, values="revenue", index="region", columns="quarter",
                        aggfunc="sum", fill_value=0, margins=True, margins_name="TOTAL")
print(matrix.applymap(lambda x: f"${x/1000:.0f}K"))""", "rw-14"),

    nb_md("### 15 · Standardising CRM Contact Data (Strings)", "rw-15-md"),
    nb_code("""\
contacts = pd.DataFrame({
    "full_name":["  alice johnson  ","BOB SMITH","DIANA Prince "],
    "email":    ["Alice@Gmail.COM "," bob@YAHOO.com","diana@corp.IO"],
    "phone":    ["(555) 123-4567","555.987.6543","+1-555-369"],
})
contacts["full_name"]    = contacts["full_name"].str.strip().str.title()
contacts["email"]        = contacts["email"].str.strip().str.lower()
contacts["email_domain"] = contacts["email"].str.extract(r"@([\w.]+)")[0]
contacts["phone_digits"] = contacts["phone"].str.replace(r"[^\\d]","",regex=True)
print(contacts.to_string(index=False))""", "rw-15"),

    nb_md("### 16 · Subscription Tenure & Renewals (DateTime)", "rw-16-md"),
    nb_code("""\
today = pd.Timestamp("2025-03-01")
subs = pd.DataFrame({
    "customer":  ["Acme","Beta","Gamma"],
    "start_date":pd.to_datetime(["2022-01-15","2024-09-01","2020-06-01"]),
    "end_date":  pd.to_datetime(["2025-03-15","2025-06-01","2025-02-28"]),
    "mrr":       [500, 99, 2000],
})
subs["tenure_months"] = ((today - subs["start_date"]).dt.days / 30).astype(int)
subs["days_to_end"]   = (subs["end_date"] - today).dt.days
subs["renewing_soon"] = subs["days_to_end"].between(0, 30)
print(subs.to_string(index=False))""", "rw-16"),

    nb_md("### 17 · Tiered Discount Engine (Apply / Map)", "rw-17-md"),
    nb_code("""\
import numpy as np
orders = pd.DataFrame({
    "order_id":[1001,1002,1003], "customer":["Alice","Bob","Charlie"],
    "subtotal":[650., 320., 95.], "vip":[True, False, False],
})
def rate(row):
    base = 0.15 if row["subtotal"]>=500 else (0.10 if row["subtotal"]>=200 else 0.05)
    return base + (0.05 if row["vip"] else 0)
orders["discount_pct"]  = orders.apply(rate, axis=1)
orders["final_price"]   = (orders["subtotal"]*(1-orders["discount_pct"])).round(2)
print(orders[["customer","subtotal","discount_pct","final_price"]].to_string(index=False))""", "rw-17"),

    nb_md("### 18 · Reshaping Survey Data for Visualisation", "rw-18-md"),
    nb_code("""\
survey = pd.DataFrame({
    "user_id":[101,102,103],
    "checkout":[4,5,3], "search":[3,4,5], "mobile":[5,5,4],
})
long = pd.melt(survey, id_vars=["user_id"], var_name="feature", value_name="rating")
print(long)
print("\\nAvg by feature:\\n", long.groupby("feature")["rating"].mean().round(2))""", "rw-18"),

    nb_md("### 19 · A/B Test Analysis (Statistics)", "rw-19-md"),
    nb_code("""\
import numpy as np
np.random.seed(42)
n=500
ab = pd.DataFrame({
    "variant":["A"]*n+["B"]*n,
    "converted":np.concatenate([np.random.binomial(1,.12,n),np.random.binomial(1,.155,n)]),
})
s = ab.groupby("variant")["converted"].agg(visitors="count",cvr="mean")
s["cvr_pct"] = (s["cvr"]*100).round(2)
print(s)
lift = (s.loc["B","cvr"]-s.loc["A","cvr"])/s.loc["A","cvr"]*100
print(f"Lift: +{lift:.1f}%")""", "rw-19"),

    nb_md("### 20 · Revenue Dashboard (Plotting)", "rw-20-md"),
    nb_code("""\
import matplotlib.pyplot as plt
monthly = pd.DataFrame({
    "Month":   pd.date_range("2024-01",periods=6,freq="ME"),
    "Revenue": [185000,210000,195000,240000,228000,265000],
    "Target":  [200000,200000,200000,220000,220000,250000],
})
monthly["MoM"] = monthly["Revenue"].pct_change()*100
fig, axes = plt.subplots(1,2,figsize=(12,4))
monthly.set_index("Month")[["Revenue","Target"]].plot(ax=axes[0],marker="o",title="Revenue vs Target")
monthly["MoM"].plot(kind="bar",ax=axes[1],color=["green" if x>0 else "red" for x in monthly["MoM"].fillna(0)],title="MoM Growth %")
plt.tight_layout(); plt.show()""", "rw-20"),

    nb_md("### 21 · Deduplicating a CRM Export", "rw-21-md"),
    nb_code("""\
crm = pd.DataFrame({
    "email":        ["alice@co.com","bob@co.com","alice@co.com"],
    "plan":         ["Pro","Basic","Pro"],
    "last_updated": ["2024-03-01","2024-01-15","2024-03-20"],
})
print(f"Before: {len(crm)} rows")
crm_clean = crm.sort_values("last_updated").drop_duplicates("email", keep="last")
print(f"After:  {len(crm_clean)} rows")
print(crm_clean.to_string(index=False))""", "rw-21"),

    nb_md("### 22 · CLV Segmentation (cut / qcut)", "rw-22-md"),
    nb_code("""\
cust = pd.DataFrame({"id":range(1001,1008),"spent":[1250,320,4500,89,780,2100,560]})
cust["tier"]  = pd.cut(cust["spent"], bins=[0,500,1500,5000], labels=["Low","Mid","High"])
cust["qtile"] = pd.qcut(cust["spent"], q=3, labels=["Q1","Q2","Q3"])
print(cust)
print("\\nRevenue by tier:")
print(cust.groupby("tier",observed=True)["spent"].sum())""", "rw-22"),

    nb_md("### 23 · ETL Pipeline (assign / pipe)", "rw-23-md"),
    nb_code("""\
import numpy as np
raw = pd.DataFrame({
    "customer":["  alice  ","BOB","charlie"], "amount":[250.,-99.,430.],
    "date":["2024-01-15","2024-01-16","2024-01-16"], "status":["completed","cancelled","completed"],
})
def clean(df):
    df=df.copy(); df["customer"]=df["customer"].str.strip().str.title(); return df
def valid(df): return df[(df["amount"]>0)]
result = (raw.pipe(clean).pipe(valid)
            .assign(date=lambda x:pd.to_datetime(x["date"]),
                    revenue=lambda x:x["amount"])
            .query("status=='completed'"))
print(result.to_string(index=False))""", "rw-23"),

    nb_md("### 24 · Fast P&L Ratios (eval)", "rw-24-md"),
    nb_code("""\
import numpy as np
np.random.seed(0)
fin = pd.DataFrame({"revenue":np.random.uniform(1e6,50e6,5),"cogs_pct":np.random.uniform(.3,.6,5),"opex_pct":np.random.uniform(.1,.2,5)})
fin.eval("cogs        = revenue * cogs_pct",inplace=True)
fin.eval("gross       = revenue - cogs",    inplace=True)
fin.eval("opex        = revenue * opex_pct",inplace=True)
fin.eval("ebit        = gross - opex",      inplace=True)
fin.eval("margin      = gross / revenue",   inplace=True)
print(fin[["revenue","gross","ebit","margin"]].round(2))""", "rw-24"),

    nb_md("### 25 · Multi-Store Inventory (MultiIndex)", "rw-25-md"),
    nb_code("""\
import numpy as np
idx = pd.MultiIndex.from_product([["NYC","LA"],["Q1","Q2","Q3","Q4"]], names=["store","quarter"])
inv = pd.DataFrame({"revenue":np.random.randint(10000,60000,len(idx))}, index=idx)
print("NYC only:\\n",     inv.loc["NYC"])
print("\\nQ4 all stores:\\n", inv.xs("Q4",level="quarter"))
print("\\nAnnual by store:\\n", inv.groupby(level="store")["revenue"].sum())""", "rw-25"),

    nb_md("### 26 · NPS Survey (Categorical)", "rw-26-md"),
    nb_code("""\
survey = pd.DataFrame({"score":[9,6,8,10,4,7,9,3,8,6]})
label = lambda s: "Promoter" if s>=9 else ("Passive" if s>=7 else "Detractor")
survey["nps"] = pd.Categorical(survey["score"].apply(label),
                               categories=["Detractor","Passive","Promoter"],ordered=True)
breakdown = survey.groupby("nps",observed=False)["score"].agg(["count","mean"]).round(2)
breakdown["pct"] = (breakdown["count"]/len(survey)*100).round(1)
print(breakdown)
print(f"NPS Index: {breakdown.loc['Promoter','pct']-breakdown.loc['Detractor','pct']:.0f}")""", "rw-26"),

    nb_md("### 27 · Stock Technical Indicators (ewm / expanding)", "rw-27-md"),
    nb_code("""\
import numpy as np
np.random.seed(42)
p = pd.Series(100+np.cumsum(np.random.normal(.2,2,30)),
              index=pd.date_range("2024-01-01",periods=30,freq="B"),name="Close")
ta = pd.DataFrame({"Close":p, "SMA_10":p.rolling(10).mean(),
                   "EMA_12":p.ewm(span=12).mean(), "ATH":p.expanding().max()})
ta["BB_upper"] = ta["SMA_10"] + 2*p.rolling(10).std()
ta["BB_lower"] = ta["SMA_10"] - 2*p.rolling(10).std()
ta["buy_sig"]  = p < ta["BB_lower"]
print(ta.tail(8).round(2))
print("Buy signals:", ta["buy_sig"].sum())""", "rw-27"),

    nb_md("### 28 · KPI Report (Styling)", "rw-28-md"),
    nb_code("""\
kpis = pd.DataFrame({
    "Metric":    ["Revenue","New Customers","Churn Rate"],
    "This Week": [285000, 142, 2.1],
    "Target":    [275000, 150, 2.0],
})
kpis["vs Target %"] = ((kpis["This Week"]-kpis["Target"])/kpis["Target"]*100).round(1)
styled = (kpis.style
    .format({"This Week":"{:,.0f}","Target":"{:,.0f}","vs Target %":"{:+.1f}%"})
    .background_gradient(subset=["vs Target %"],cmap="RdYlGn",vmin=-10,vmax=10)
    .hide(axis="index"))
# In Jupyter: styled renders as a coloured table
print(kpis.to_string(index=False))""", "rw-28"),

    nb_md("### 29 · Memory Optimisation", "rw-29-md"),
    nb_code("""\
import numpy as np
np.random.seed(0); n=200_000
txn = pd.DataFrame({"id":np.arange(n),"cat":np.random.choice(["A","B","C"],n),
                    "val":np.random.uniform(1,500,n),"flag":np.random.randint(0,2,n)})
before = txn.memory_usage(deep=True).sum()/1e6
txn["id"]  = txn["id"].astype("uint32")
txn["cat"] = txn["cat"].astype("category")
txn["val"] = txn["val"].astype("float32")
txn["flag"]= txn["flag"].astype("int8")
after = txn.memory_usage(deep=True).sum()/1e6
print(f"Before: {before:.1f}MB  →  After: {after:.1f}MB  (saved {(1-after/before)*100:.0f}%)")""", "rw-29"),

    nb_md("### 30 · Stratified Train/Test Split (Sampling)", "rw-30-md"),
    nb_code("""\
import numpy as np
np.random.seed(42); n=500
df = pd.DataFrame({"feat":np.random.rand(n),"churn":np.random.choice([0,1],n,p=[.8,.2])})
train = df.groupby("churn",group_keys=False).apply(lambda x:x.sample(frac=.7,random_state=42))
test  = df.drop(train.index)
for nm,sp in [("Train",train),("Test",test)]:
    print(f"{nm}: {len(sp)} rows | churn={sp['churn'].mean():.1%}")""", "rw-30"),

    nb_md("### 31 · Portfolio Returns & Drawdown (shift / diff)", "rw-31-md"),
    nb_code("""\
import numpy as np
np.random.seed(1)
nav = pd.Series([10000]+list(10000*np.cumprod(1+np.random.normal(.0005,.015,29))),
                index=pd.date_range("2024-01-02",periods=30,freq="B"),name="NAV")
pf = pd.DataFrame({"NAV":nav})
pf["daily_ret"]  = pf["NAV"].pct_change()
pf["cum_ret_%"]  = (pf["NAV"]/pf["NAV"].iloc[0]-1)*100
pf["rolling_max"]= pf["NAV"].expanding().max()
pf["drawdown_%"] = (pf["NAV"]-pf["rolling_max"])/pf["rolling_max"]*100
sharpe = pf["daily_ret"].mean()/pf["daily_ret"].std()*252**0.5
print(pf.tail(5).round(3))
print(f"Sharpe: {sharpe:.2f}  |  Max DD: {pf['drawdown_%'].min():.2f}%")""", "rw-31"),

    nb_md("### 32 · Expand Cart Items (explode)", "rw-32-md"),
    nb_code("""\
orders = pd.DataFrame({
    "order_id":[5001,5002,5003],
    "items":[["USB-Hub","Webcam","Mouse"],["Keyboard","Mouse"],["Monitor","USB-Hub","Webcam"]],
})
items = orders.explode("items").rename(columns={"items":"product"}).reset_index(drop=True)
print(items)
print("\\nTop products:")
print(items["product"].value_counts())""", "rw-32"),
]

nb["cells"].extend(NB_RW)

with open(NB_FILE, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Notebook updated — {len(NB_RW)} cells added ({len(nb['cells'])} total).")
