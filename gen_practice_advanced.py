import json, os

OUT = r"c:\Users\seany\Documents\All Codes\Python Panda Library Study"

def md(src): return {"cell_type":"markdown","metadata":{},"source":[src]}
def code(src): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[src]}

cells = []

cells.append(md(
    "# 🐼 Pandas Practice — Advanced Exercises (11–20)\n\n"
    "Continuation of the practice series covering advanced pandas features.\n\n"
    "| Exercise | Topic |\n"
    "|----------|-------|\n"
    "| 11 | Reshaping — melt, stack, unstack |\n"
    "| 12 | MultiIndex |\n"
    "| 13 | Categorical Data |\n"
    "| 14 | Method Chaining — assign() & pipe() |\n"
    "| 15 | eval() & query() |\n"
    "| 16 | shift() & diff() — Lag Analysis |\n"
    "| 17 | explode() — List Columns |\n"
    "| 18 | Memory Optimization |\n"
    "| 19 | Sampling & Bootstrap |\n"
    "| 20 | RFM Customer Segmentation (Mini Project) |\n\n"
    "---"
))

cells.append(md("## Setup"))
cells.append(code(
    "import pandas as pd\n"
    "import numpy as np\n"
    "np.random.seed(42)\n"
    "print('pandas:', pd.__version__)"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 11 — Reshaping
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 11 — Reshaping: melt, stack, unstack\n\n"
    "**Scenario:** Transform a wide quarterly sales report into long format and back.\n\n"
    "Tasks:\n"
    "1. Use `melt()` to convert the wide format into long format with columns `region`, `quarter`, `sales`\n"
    "2. Use `pivot()` to convert back to wide format\n"
    "3. Use `stack()` on a MultiIndex DataFrame to get a Series\n"
    "4. Use `unstack()` to convert back to DataFrame\n"
    "5. Find the quarter with the highest average sales across all regions"
))
cells.append(code(
    "wide = pd.DataFrame({\n"
    "    'region': ['North', 'South', 'East', 'West'],\n"
    "    'Q1': [120000, 95000, 140000, 110000],\n"
    "    'Q2': [130000, 98000, 155000, 118000],\n"
    "    'Q3': [145000, 102000, 160000, 125000],\n"
    "    'Q4': [160000, 115000, 175000, 138000],\n"
    "})\n"
    "print('Wide format:')\n"
    "print(wide)\n\n"
    "# 1. melt to long format\n"
    "# YOUR CODE HERE\n\n"
    "# 2. pivot back to wide\n"
    "# YOUR CODE HERE\n\n"
    "# 3. stack example\n"
    "df_mi = wide.set_index('region')\n"
    "# YOUR CODE HERE (stack df_mi)\n\n"
    "# 4. unstack\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Best quarter by avg sales\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 12 — MultiIndex
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 12 — MultiIndex\n\n"
    "**Scenario:** Work with a hierarchical index for a stock portfolio.\n\n"
    "Tasks:\n"
    "1. Create a MultiIndex DataFrame with `(ticker, date)` as the index\n"
    "2. Select all rows for ticker `'AAPL'`\n"
    "3. Select `AAPL` on `2024-01-03`\n"
    "4. Use `xs()` to cross-section by date across all tickers\n"
    "5. Reset the index and group by `ticker` to get mean `close` price"
))
cells.append(code(
    "tickers = ['AAPL', 'GOOG', 'MSFT']\n"
    "dates = pd.date_range('2024-01-01', periods=5, freq='B')\n"
    "idx = pd.MultiIndex.from_product([tickers, dates], names=['ticker', 'date'])\n"
    "np.random.seed(1)\n"
    "portfolio = pd.DataFrame({\n"
    "    'open':  np.random.uniform(100, 400, len(idx)).round(2),\n"
    "    'close': np.random.uniform(100, 400, len(idx)).round(2),\n"
    "    'volume': np.random.randint(1_000_000, 50_000_000, len(idx))\n"
    "}, index=idx)\n"
    "print(portfolio.head(8))\n\n"
    "# 2. All AAPL rows\n"
    "# YOUR CODE HERE\n\n"
    "# 3. AAPL on 2024-01-03\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Cross-section by date 2024-01-02\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Reset index + mean close per ticker\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 13 — Categorical Data
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 13 — Categorical Data\n\n"
    "**Scenario:** Work with ordered survey responses to analyse satisfaction levels.\n\n"
    "Tasks:\n"
    "1. Convert `rating` to an ordered Categorical: `Very Poor < Poor < Neutral < Good < Excellent`\n"
    "2. Count responses per rating (respects order)\n"
    "3. Filter for ratings `>= Good`\n"
    "4. Add a `score` column: Very Poor=1, Poor=2, Neutral=3, Good=4, Excellent=5\n"
    "5. Check memory savings vs plain object dtype"
))
cells.append(code(
    "np.random.seed(5)\n"
    "n = 500\n"
    "survey = pd.DataFrame({\n"
    "    'respondent_id': range(1, n+1),\n"
    "    'dept': np.random.choice(['Eng','Sales','HR','Finance'], n),\n"
    "    'rating': np.random.choice(['Very Poor','Poor','Neutral','Good','Excellent'], n,\n"
    "                               p=[0.05, 0.10, 0.25, 0.40, 0.20]),\n"
    "})\n\n"
    "# 1. Ordered Categorical\n"
    "order = ['Very Poor', 'Poor', 'Neutral', 'Good', 'Excellent']\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Value counts (ordered)\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Filter >= Good\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Numeric score column\n"
    "score_map = {'Very Poor':1, 'Poor':2, 'Neutral':3, 'Good':4, 'Excellent':5}\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Memory comparison\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 14 — Method Chaining
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 14 — Method Chaining with assign() & pipe()\n\n"
    "**Scenario:** Build a clean, readable ETL pipeline using method chaining.\n\n"
    "Tasks:\n"
    "1. In a single chain: filter active users, add `full_name`, add `age_group` (bins: 18-30, 31-45, 46+), sort by `ltv` desc\n"
    "2. Write a `normalize_ltv(df)` function and apply it with `pipe()`\n"
    "3. Use `assign()` to add `revenue_per_day = ltv / tenure_days` in the chain\n"
    "4. Chain `query()` to keep only users with `revenue_per_day > 1`\n"
    "5. Print the final shape and first 5 rows"
))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 300\n"
    "users = pd.DataFrame({\n"
    "    'user_id': range(1, n+1),\n"
    "    'first': np.random.choice(['Alice','Bob','Carol','Dave','Eve'], n),\n"
    "    'last':  np.random.choice(['Smith','Jones','Lee','Brown','Taylor'], n),\n"
    "    'age':   np.random.randint(18, 65, n),\n"
    "    'active': np.random.choice([True, False], n, p=[0.8, 0.2]),\n"
    "    'ltv':    np.random.exponential(500, n).round(2),\n"
    "    'tenure_days': np.random.randint(1, 1000, n),\n"
    "})\n\n"
    "# 2. pipe helper\n"
    "def normalize_ltv(df):\n"
    "    df = df.copy()\n"
    "    df['ltv_normalized'] = (df['ltv'] - df['ltv'].min()) / (df['ltv'].max() - df['ltv'].min())\n"
    "    return df\n\n"
    "# 1, 3, 4 — full chain\n"
    "result = (\n"
    "    users\n"
    "    # YOUR CODE HERE: filter active\n"
    "    # YOUR CODE HERE: assign full_name, age_group, revenue_per_day\n"
    "    # YOUR CODE HERE: pipe normalize_ltv\n"
    "    # YOUR CODE HERE: query revenue_per_day > 1\n"
    "    # YOUR CODE HERE: sort by ltv desc\n"
    ")\n\n"
    "# 5.\n"
    "print('Shape:', result.shape)\n"
    "print(result[['full_name','age_group','ltv','revenue_per_day','ltv_normalized']].head())"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 15 — eval() & query()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 15 — eval() & query()\n\n"
    "**Scenario:** Analyse financial data efficiently using pandas expressions.\n\n"
    "Tasks:\n"
    "1. Use `query()` to filter rows where `pe_ratio < 20` AND `market_cap > 10`\n"
    "2. Use `query()` with a Python variable: filter where `dividend_yield > threshold`\n"
    "3. Use `eval()` to compute `enterprise_value = market_cap + total_debt - cash`\n"
    "4. Use `eval()` to compute `ev_ebitda = enterprise_value / ebitda` in one expression\n"
    "5. Compare performance: `eval()` vs standard pandas for adding two columns on 500K rows"
))
cells.append(code(
    "np.random.seed(3)\n"
    "n = 200\n"
    "stocks = pd.DataFrame({\n"
    "    'ticker':         [f'TKR{i:03d}' for i in range(n)],\n"
    "    'market_cap':     np.random.uniform(1, 500, n).round(2),   # billions\n"
    "    'pe_ratio':       np.random.uniform(5, 60, n).round(1),\n"
    "    'dividend_yield': np.random.uniform(0, 8, n).round(2),\n"
    "    'total_debt':     np.random.uniform(0, 100, n).round(2),\n"
    "    'cash':           np.random.uniform(0, 50, n).round(2),\n"
    "    'ebitda':         np.random.uniform(0.5, 50, n).round(2),\n"
    "})\n\n"
    "# 1. query: pe < 20 AND market_cap > 10\n"
    "# YOUR CODE HERE\n\n"
    "# 2. query with variable\n"
    "threshold = 3.0\n"
    "# YOUR CODE HERE\n\n"
    "# 3. eval enterprise_value\n"
    "# YOUR CODE HERE\n\n"
    "# 4. eval ev_ebitda (chain or use inplace)\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Performance comparison on large df\n"
    "import time\n"
    "big = pd.DataFrame({'a': np.random.randn(500_000), 'b': np.random.randn(500_000)})\n"
    "t0 = time.time(); _ = big['a'] + big['b']; t_std = time.time() - t0\n"
    "t0 = time.time(); _ = big.eval('a + b');    t_ev  = time.time() - t0\n"
    "print(f'Standard: {t_std*1000:.2f}ms  |  eval: {t_ev*1000:.2f}ms')"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 16 — shift() & diff()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 16 — shift() & diff() — Lag Analysis\n\n"
    "**Scenario:** Analyse month-over-month and year-over-year changes in revenue.\n\n"
    "Tasks:\n"
    "1. Add `prev_month_revenue` using `shift(1)`\n"
    "2. Add `mom_change` (month-over-month absolute change) using `diff()`\n"
    "3. Add `mom_pct` (month-over-month % change)\n"
    "4. Add `yoy_change` by shifting 12 periods\n"
    "5. Flag months where revenue dropped more than 10% MoM"
))
cells.append(code(
    "months = pd.date_range('2022-01-01', periods=36, freq='MS')\n"
    "np.random.seed(9)\n"
    "base = 100_000\n"
    "trend = np.linspace(0, 30000, 36)\n"
    "seasonal = 15000 * np.sin(np.linspace(0, 4*np.pi, 36))\n"
    "noise = np.random.normal(0, 5000, 36)\n"
    "revenue_data = pd.DataFrame({\n"
    "    'month': months,\n"
    "    'revenue': (base + trend + seasonal + noise).round(0).astype(int)\n"
    "})\n"
    "revenue_data = revenue_data.set_index('month')\n"
    "print(revenue_data.head())\n\n"
    "# 1. prev_month_revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 2. mom_change\n"
    "# YOUR CODE HERE\n\n"
    "# 3. mom_pct\n"
    "# YOUR CODE HERE\n\n"
    "# 4. yoy_change (shift 12)\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Flag drops > 10% MoM\n"
    "# YOUR CODE HERE\n\n"
    "print(revenue_data.tail(10))"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 17 — explode()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 17 — explode() with List Columns\n\n"
    "**Scenario:** A product database stores multiple tags and categories per item as lists.\n\n"
    "Tasks:\n"
    "1. Use `explode()` to expand the `tags` list column into one row per tag\n"
    "2. Count how many products have each tag\n"
    "3. Find the top 5 most common tags\n"
    "4. Explode `sizes` and count available size options per category\n"
    "5. Find products that have both `'wireless'` AND `'bluetooth'` tags"
))
cells.append(code(
    "products = pd.DataFrame({\n"
    "    'product_id': [1, 2, 3, 4, 5, 6],\n"
    "    'name': ['Headphones','Keyboard','Mouse','Speaker','Webcam','Monitor'],\n"
    "    'category': ['Audio','Input','Input','Audio','Video','Video'],\n"
    "    'price': [79.99, 49.99, 29.99, 99.99, 59.99, 299.99],\n"
    "    'tags': [\n"
    "        ['wireless','bluetooth','noise-cancelling'],\n"
    "        ['mechanical','rgb','wireless'],\n"
    "        ['wireless','ergonomic','silent'],\n"
    "        ['bluetooth','waterproof','portable'],\n"
    "        ['hd','usb','plug-and-play'],\n"
    "        ['4k','hdr','usb-c','bluetooth'],\n"
    "    ],\n"
    "    'sizes': [['S','M','L'],['M','L'],['S','M'],['M','L','XL'],['M'],['L','XL']]\n"
    "})\n\n"
    "# 1. explode tags\n"
    "# YOUR CODE HERE\n\n"
    "# 2. count per tag\n"
    "# YOUR CODE HERE\n\n"
    "# 3. top 5 tags\n"
    "# YOUR CODE HERE\n\n"
    "# 4. explode sizes + count per category\n"
    "# YOUR CODE HERE\n\n"
    "# 5. products with both 'wireless' AND 'bluetooth'\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 18 — Memory Optimization
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 18 — Memory Optimization\n\n"
    "**Scenario:** A 500K row dataset is consuming too much RAM — optimize it.\n\n"
    "Tasks:\n"
    "1. Check memory usage per column with `memory_usage(deep=True)`\n"
    "2. Downcast integer columns to the smallest type that fits (`pd.to_numeric` with `downcast`)\n"
    "3. Downcast float columns similarly\n"
    "4. Convert low-cardinality string columns to `category` dtype\n"
    "5. Report total memory before and after, and the % reduction"
))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 500_000\n"
    "df = pd.DataFrame({\n"
    "    'user_id':   np.random.randint(0, 100_000, n),         # int64\n"
    "    'age':       np.random.randint(18, 90, n),              # int64 but fits int8\n"
    "    'score':     np.random.uniform(0, 100, n),              # float64 but float32 ok\n"
    "    'rating':    np.random.randint(1, 6, n),                # int64 but fits int8\n"
    "    'country':   np.random.choice(['US','UK','DE','JP','BR'], n),  # object\n"
    "    'plan':      np.random.choice(['free','basic','pro','enterprise'], n),  # object\n"
    "    'revenue':   np.random.exponential(100, n),             # float64\n"
    "})\n\n"
    "mem_before = df.memory_usage(deep=True).sum() / 1024**2\n"
    "print(f'Memory before: {mem_before:.2f} MB')\n"
    "print(df.dtypes)\n\n"
    "# 2. Downcast integers\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Downcast floats\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Convert string cols to category\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Report savings\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 19 — Sampling & Bootstrap
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 19 — Sampling & Bootstrap Confidence Intervals\n\n"
    "**Scenario:** Estimate the true average order value with confidence intervals using bootstrap resampling.\n\n"
    "Tasks:\n"
    "1. Draw a random sample of 200 rows (without replacement) — set `random_state=42`\n"
    "2. Draw a stratified sample: 50 rows per `channel`, proportional to channel size\n"
    "3. Bootstrap the mean of `order_value` — resample with replacement 1000 times, store each mean\n"
    "4. Compute the 95% confidence interval from the bootstrap distribution\n"
    "5. Compare the sample mean to the true population mean"
))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 10_000\n"
    "orders = pd.DataFrame({\n"
    "    'order_id':    range(n),\n"
    "    'channel':     np.random.choice(['Web','Mobile','In-Store','Phone'], n, p=[0.5,0.3,0.15,0.05]),\n"
    "    'order_value': np.random.exponential(75, n).round(2),\n"
    "    'region':      np.random.choice(['North','South','East','West'], n),\n"
    "})\n"
    "print('Population mean order value:', orders['order_value'].mean().round(2))\n\n"
    "# 1. Simple random sample\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Stratified sample: 50 per channel\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Bootstrap 1000 iterations\n"
    "# YOUR CODE HERE\n\n"
    "# 4. 95% CI\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Compare\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 20 — Mini Project: RFM Segmentation
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 20 — Mini Project: RFM Customer Segmentation\n\n"
    "**Scenario:** Segment customers using the classic **RFM model** (Recency, Frequency, Monetary).\n\n"
    "RFM scores each customer 1–4 on three dimensions:\n"
    "- **Recency**: how recently they bought (4 = most recent)\n"
    "- **Frequency**: how often they buy (4 = most frequent)\n"
    "- **Monetary**: how much they spend (4 = highest spender)\n\n"
    "Tasks:\n"
    "1. Compute RFM metrics per customer: last purchase date, number of orders, total spend\n"
    "2. Score each metric 1–4 using `pd.qcut()` (quartiles)\n"
    "3. Create `rfm_score` = concatenation of R, F, M scores as a string (e.g. `'444'`)\n"
    "4. Map scores to segments: Champions (444,443,434), Loyal (334,343,344), At Risk (244,234,224), Lost (111,112,121,122)\n"
    "5. Count customers per segment and calculate avg total spend per segment\n"
    "6. Print a summary table sorted by avg spend desc"
))
cells.append(code(
    "from datetime import date\n\n"
    "np.random.seed(42)\n"
    "n_customers = 500\n"
    "n_orders = 3000\n"
    "snapshot_date = pd.Timestamp('2024-12-31')\n\n"
    "transactions = pd.DataFrame({\n"
    "    'customer_id': np.random.choice([f'C{i:04d}' for i in range(n_customers)], n_orders),\n"
    "    'order_date':  pd.to_datetime(np.random.choice(\n"
    "        pd.date_range('2023-01-01', '2024-12-31').astype(str), n_orders\n"
    "    )),\n"
    "    'order_value': np.random.exponential(80, n_orders).round(2)\n"
    "})\n\n"
    "# 1. RFM metrics\n"
    "# YOUR CODE HERE\n"
    "# rfm = transactions.groupby('customer_id').agg(...)\n\n"
    "# 2. Score 1-4 using qcut\n"
    "# Recency: lower days = better = score 4\n"
    "# Frequency & Monetary: higher = better = score 4\n"
    "# YOUR CODE HERE\n\n"
    "# 3. rfm_score string\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Segment mapping\n"
    "champions   = ['444','443','434','344']\n"
    "loyal       = ['334','343','333','324','342']\n"
    "at_risk     = ['244','234','224','243','242']\n"
    "lost        = ['111','112','121','122','211','212']\n"
    "\n"
    "def map_segment(score):\n"
    "    if score in champions: return 'Champions'\n"
    "    if score in loyal:     return 'Loyal'\n"
    "    if score in at_risk:   return 'At Risk'\n"
    "    if score in lost:      return 'Lost'\n"
    "    return 'Others'\n\n"
    "# YOUR CODE HERE (apply map_segment)\n\n"
    "# 5 & 6. Summary\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# SOLUTIONS
# ══════════════════════════════════════════════════════════════════════════
cells.append(md("---\n# ✅ Solutions (11–20)\n\n> Try first!"))

# Sol 11
cells.append(md("## Solution 11 — Reshaping"))
cells.append(code(
    "wide = pd.DataFrame({'region':['North','South','East','West'],'Q1':[120000,95000,140000,110000],'Q2':[130000,98000,155000,118000],'Q3':[145000,102000,160000,125000],'Q4':[160000,115000,175000,138000]})\n"
    "long = wide.melt(id_vars='region', var_name='quarter', value_name='sales')\n"
    "print('Long:'); print(long.head(6))\n"
    "wide2 = long.pivot(index='region', columns='quarter', values='sales')\n"
    "print('Wide back:'); print(wide2)\n"
    "stacked = wide.set_index('region').stack()\n"
    "print('Stacked:'); print(stacked.head(6))\n"
    "unstacked = stacked.unstack()\n"
    "print('Unstacked:'); print(unstacked)\n"
    "best_q = long.groupby('quarter')['sales'].mean().idxmax()\n"
    "print('Best quarter:', best_q)"
))

# Sol 12
cells.append(md("## Solution 12 — MultiIndex"))
cells.append(code(
    "tickers = ['AAPL','GOOG','MSFT']\n"
    "dates = pd.date_range('2024-01-01', periods=5, freq='B')\n"
    "idx = pd.MultiIndex.from_product([tickers, dates], names=['ticker','date'])\n"
    "np.random.seed(1)\n"
    "portfolio = pd.DataFrame({'open':np.random.uniform(100,400,len(idx)).round(2),'close':np.random.uniform(100,400,len(idx)).round(2),'volume':np.random.randint(1_000_000,50_000_000,len(idx))}, index=idx)\n"
    "print(portfolio.loc['AAPL'])\n"
    "print(portfolio.loc[('AAPL', '2024-01-03')])\n"
    "print(portfolio.xs('2024-01-02', level='date'))\n"
    "print(portfolio.reset_index().groupby('ticker')['close'].mean().round(2))"
))

# Sol 13
cells.append(md("## Solution 13 — Categorical Data"))
cells.append(code(
    "np.random.seed(5)\n"
    "n = 500\n"
    "survey = pd.DataFrame({'respondent_id':range(1,n+1),'dept':np.random.choice(['Eng','Sales','HR','Finance'],n),'rating':np.random.choice(['Very Poor','Poor','Neutral','Good','Excellent'],n,p=[0.05,0.10,0.25,0.40,0.20])})\n"
    "order = ['Very Poor','Poor','Neutral','Good','Excellent']\n"
    "survey['rating'] = pd.Categorical(survey['rating'], categories=order, ordered=True)\n"
    "print(survey['rating'].value_counts().sort_index())\n"
    "print(survey[survey['rating'] >= 'Good'].shape)\n"
    "score_map = {'Very Poor':1,'Poor':2,'Neutral':3,'Good':4,'Excellent':5}\n"
    "survey['score'] = survey['rating'].map(score_map)\n"
    "obj_mem = survey['rating'].astype(str).memory_usage(deep=True)\n"
    "cat_mem = survey['rating'].memory_usage(deep=True)\n"
    "print(f'Object: {obj_mem} bytes | Category: {cat_mem} bytes | Saved: {obj_mem-cat_mem} bytes')"
))

# Sol 14
cells.append(md("## Solution 14 — Method Chaining"))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 300\n"
    "users = pd.DataFrame({'user_id':range(1,n+1),'first':np.random.choice(['Alice','Bob','Carol','Dave','Eve'],n),'last':np.random.choice(['Smith','Jones','Lee','Brown','Taylor'],n),'age':np.random.randint(18,65,n),'active':np.random.choice([True,False],n,p=[0.8,0.2]),'ltv':np.random.exponential(500,n).round(2),'tenure_days':np.random.randint(1,1000,n)})\n"
    "def normalize_ltv(df):\n"
    "    df = df.copy()\n"
    "    df['ltv_normalized'] = (df['ltv'] - df['ltv'].min()) / (df['ltv'].max() - df['ltv'].min())\n"
    "    return df\n"
    "result = (\n"
    "    users\n"
    "    .query('active == True')\n"
    "    .assign(\n"
    "        full_name = lambda d: d['first'] + ' ' + d['last'],\n"
    "        age_group = lambda d: pd.cut(d['age'], bins=[17,30,45,100], labels=['18-30','31-45','46+']),\n"
    "        revenue_per_day = lambda d: (d['ltv'] / d['tenure_days']).round(4)\n"
    "    )\n"
    "    .pipe(normalize_ltv)\n"
    "    .query('revenue_per_day > 1')\n"
    "    .sort_values('ltv', ascending=False)\n"
    ")\n"
    "print('Shape:', result.shape)\n"
    "print(result[['full_name','age_group','ltv','revenue_per_day','ltv_normalized']].head())"
))

# Sol 15
cells.append(md("## Solution 15 — eval() & query()"))
cells.append(code(
    "np.random.seed(3)\n"
    "n = 200\n"
    "stocks = pd.DataFrame({'ticker':[f'TKR{i:03d}' for i in range(n)],'market_cap':np.random.uniform(1,500,n).round(2),'pe_ratio':np.random.uniform(5,60,n).round(1),'dividend_yield':np.random.uniform(0,8,n).round(2),'total_debt':np.random.uniform(0,100,n).round(2),'cash':np.random.uniform(0,50,n).round(2),'ebitda':np.random.uniform(0.5,50,n).round(2)})\n"
    "print(stocks.query('pe_ratio < 20 and market_cap > 10').shape)\n"
    "threshold = 3.0\n"
    "print(stocks.query('dividend_yield > @threshold').shape)\n"
    "stocks.eval('enterprise_value = market_cap + total_debt - cash', inplace=True)\n"
    "stocks.eval('ev_ebitda = enterprise_value / ebitda', inplace=True)\n"
    "print(stocks[['ticker','enterprise_value','ev_ebitda']].head())\n"
    "import time\n"
    "big = pd.DataFrame({'a':np.random.randn(500_000),'b':np.random.randn(500_000)})\n"
    "t0 = time.time(); _ = big['a']+big['b']; print(f'Standard: {(time.time()-t0)*1000:.2f}ms')\n"
    "t0 = time.time(); _ = big.eval('a+b');   print(f'eval:     {(time.time()-t0)*1000:.2f}ms')"
))

# Sol 16
cells.append(md("## Solution 16 — shift() & diff()"))
cells.append(code(
    "months = pd.date_range('2022-01-01', periods=36, freq='MS')\n"
    "np.random.seed(9)\n"
    "base=100_000; trend=np.linspace(0,30000,36); seasonal=15000*np.sin(np.linspace(0,4*np.pi,36)); noise=np.random.normal(0,5000,36)\n"
    "revenue_data = pd.DataFrame({'revenue':(base+trend+seasonal+noise).round(0).astype(int)}, index=months)\n"
    "revenue_data['prev_month_revenue'] = revenue_data['revenue'].shift(1)\n"
    "revenue_data['mom_change'] = revenue_data['revenue'].diff()\n"
    "revenue_data['mom_pct'] = revenue_data['revenue'].pct_change().round(4)\n"
    "revenue_data['yoy_change'] = revenue_data['revenue'].diff(12)\n"
    "revenue_data['big_drop'] = revenue_data['mom_pct'] < -0.10\n"
    "print(revenue_data.tail(10))\n"
    "print('Big drops:', revenue_data['big_drop'].sum())"
))

# Sol 17
cells.append(md("## Solution 17 — explode()"))
cells.append(code(
    "products = pd.DataFrame({'product_id':[1,2,3,4,5,6],'name':['Headphones','Keyboard','Mouse','Speaker','Webcam','Monitor'],'category':['Audio','Input','Input','Audio','Video','Video'],'price':[79.99,49.99,29.99,99.99,59.99,299.99],'tags':[['wireless','bluetooth','noise-cancelling'],['mechanical','rgb','wireless'],['wireless','ergonomic','silent'],['bluetooth','waterproof','portable'],['hd','usb','plug-and-play'],['4k','hdr','usb-c','bluetooth']],'sizes':[['S','M','L'],['M','L'],['S','M'],['M','L','XL'],['M'],['L','XL']]})\n"
    "exploded_tags = products.explode('tags')\n"
    "print(exploded_tags[['name','tags']].head(8))\n"
    "tag_counts = exploded_tags['tags'].value_counts()\n"
    "print('Top 5 tags:')\n"
    "print(tag_counts.head(5))\n"
    "sizes_by_cat = products.explode('sizes').groupby('category')['sizes'].count()\n"
    "print('Size options per category:')\n"
    "print(sizes_by_cat)\n"
    "has_wireless = set(products[products['tags'].apply(lambda t: 'wireless' in t)]['product_id'])\n"
    "has_bluetooth = set(products[products['tags'].apply(lambda t: 'bluetooth' in t)]['product_id'])\n"
    "both = has_wireless & has_bluetooth\n"
    "print('Both wireless & bluetooth:', products[products['product_id'].isin(both)]['name'].tolist())"
))

# Sol 18
cells.append(md("## Solution 18 — Memory Optimization"))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 500_000\n"
    "df = pd.DataFrame({'user_id':np.random.randint(0,100_000,n),'age':np.random.randint(18,90,n),'score':np.random.uniform(0,100,n),'rating':np.random.randint(1,6,n),'country':np.random.choice(['US','UK','DE','JP','BR'],n),'plan':np.random.choice(['free','basic','pro','enterprise'],n),'revenue':np.random.exponential(100,n)})\n"
    "mem_before = df.memory_usage(deep=True).sum() / 1024**2\n"
    "for col in ['user_id','age','rating']:\n"
    "    df[col] = pd.to_numeric(df[col], downcast='integer')\n"
    "for col in ['score','revenue']:\n"
    "    df[col] = pd.to_numeric(df[col], downcast='float')\n"
    "for col in ['country','plan']:\n"
    "    df[col] = df[col].astype('category')\n"
    "mem_after = df.memory_usage(deep=True).sum() / 1024**2\n"
    "print(f'Before: {mem_before:.2f} MB')\n"
    "print(f'After:  {mem_after:.2f} MB')\n"
    "print(f'Saved:  {mem_before-mem_after:.2f} MB ({(1-mem_after/mem_before)*100:.1f}% reduction)')\n"
    "print(df.dtypes)"
))

# Sol 19
cells.append(md("## Solution 19 — Sampling & Bootstrap"))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 10_000\n"
    "orders = pd.DataFrame({'order_id':range(n),'channel':np.random.choice(['Web','Mobile','In-Store','Phone'],n,p=[0.5,0.3,0.15,0.05]),'order_value':np.random.exponential(75,n).round(2),'region':np.random.choice(['North','South','East','West'],n)})\n"
    "pop_mean = orders['order_value'].mean()\n"
    "sample = orders.sample(200, random_state=42)\n"
    "print('Sample mean:', sample['order_value'].mean().round(2), '| Pop mean:', pop_mean.round(2))\n"
    "strat = orders.groupby('channel', group_keys=False).apply(lambda x: x.sample(50, random_state=42))\n"
    "print('Stratified sample shape:', strat.shape)\n"
    "boot_means = [orders['order_value'].sample(200, replace=True).mean() for _ in range(1000)]\n"
    "boot_series = pd.Series(boot_means)\n"
    "ci_low  = boot_series.quantile(0.025).round(2)\n"
    "ci_high = boot_series.quantile(0.975).round(2)\n"
    "print(f'Bootstrap mean: {boot_series.mean():.2f}')\n"
    "print(f'95% CI: [{ci_low}, {ci_high}]')\n"
    "print(f'True population mean inside CI: {ci_low <= pop_mean <= ci_high}')"
))

# Sol 20
cells.append(md("## Solution 20 — RFM Customer Segmentation"))
cells.append(code(
    "np.random.seed(42)\n"
    "n_customers=500; n_orders=3000\n"
    "snapshot_date = pd.Timestamp('2024-12-31')\n"
    "transactions = pd.DataFrame({'customer_id':np.random.choice([f'C{i:04d}' for i in range(n_customers)],n_orders),'order_date':pd.to_datetime(np.random.choice(pd.date_range('2023-01-01','2024-12-31').astype(str),n_orders)),'order_value':np.random.exponential(80,n_orders).round(2)})\n\n"
    "rfm = transactions.groupby('customer_id').agg(\n"
    "    recency   = ('order_date', lambda x: (snapshot_date - x.max()).days),\n"
    "    frequency = ('order_id',   'count') if 'order_id' in transactions else ('order_value','count'),\n"
    "    monetary  = ('order_value','sum')\n"
    ").round(2)\n\n"
    "rfm['R'] = pd.qcut(rfm['recency'],   q=4, labels=[4,3,2,1]).astype(int)\n"
    "rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'), q=4, labels=[1,2,3,4]).astype(int)\n"
    "rfm['M'] = pd.qcut(rfm['monetary'],  q=4, labels=[1,2,3,4]).astype(int)\n"
    "rfm['rfm_score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)\n\n"
    "champions=['444','443','434','344']; loyal=['334','343','333','324','342']\n"
    "at_risk=['244','234','224','243','242']; lost=['111','112','121','122','211','212']\n"
    "def map_segment(s):\n"
    "    if s in champions: return 'Champions'\n"
    "    if s in loyal:     return 'Loyal'\n"
    "    if s in at_risk:   return 'At Risk'\n"
    "    if s in lost:      return 'Lost'\n"
    "    return 'Others'\n"
    "rfm['segment'] = rfm['rfm_score'].apply(map_segment)\n\n"
    "summary = rfm.groupby('segment').agg(\n"
    "    customers=('monetary','count'),\n"
    "    avg_spend=('monetary','mean'),\n"
    "    avg_frequency=('frequency','mean')\n"
    ").round(2).sort_values('avg_spend', ascending=False)\n"
    "print('RFM Segment Summary:')\n"
    "print(summary)"
))

# Write notebook
nb = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
        "language_info": {"name":"python","version":"3.10.0"}
    },
    "cells": cells
}

path = os.path.join(OUT, "pandas_practice_advanced.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

size_kb = os.path.getsize(path) / 1024
print(f"Created: {path}")
print(f"  {len(cells)} cells | {size_kb:.1f} KB")
print(f"  10 advanced exercises + 10 solutions")
