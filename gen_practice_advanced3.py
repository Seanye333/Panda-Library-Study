import json, os

OUT = r"c:\Users\seany\Documents\All Codes\Python Panda Library Study"

def md(src): return {"cell_type":"markdown","metadata":{},"source":[src]}
def code(src): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[src]}

cells = []

cells.append(md(
    "# 🐼 Pandas Practice — Expert Exercises (21–40)\n\n"
    "Advanced pandas patterns used in real data engineering and analysis work.\n\n"
    "| Exercise | Topic |\n"
    "|----------|-------|\n"
    "| 21 | Time Series Resampling |\n"
    "| 22 | crosstab() & Contingency Tables |\n"
    "| 23 | Custom Aggregation with agg() |\n"
    "| 24 | where() & mask() — Conditional Updates |\n"
    "| 25 | merge() with indicator & many-to-many |\n"
    "| 26 | wide_to_long() |\n"
    "| 27 | Advanced String Ops (regex extract, findall) |\n"
    "| 28 | DateTime Advanced (tz, offsets, holidays) |\n"
    "| 29 | Chunked CSV Processing |\n"
    "| 30 | Rolling & Expanding Advanced |\n"
    "| 31 | groupby + transform (broadcast) |\n"
    "| 32 | apply() axis=1 vs vectorized |\n"
    "| 33 | Hierarchical GroupBy |\n"
    "| 34 | merge_asof() — Time-Based Join |\n"
    "| 35 | pivot_table() with margins & aggfunc |\n"
    "| 36 | DataFrame.compare() |\n"
    "| 37 | pd.json_normalize() — Nested JSON |\n"
    "| 38 | IntervalIndex & pd.cut advanced |\n"
    "| 39 | GroupBy + cumulative stats |\n"
    "| 40 | Mini Project: End-to-End Sales Pipeline |\n\n"
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
# Exercise 21 — Time Series Resampling
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 21 — Time Series Resampling\n\n"
    "**Scenario:** You have hourly sensor readings for 60 days. Analyse at multiple time scales.\n\n"
    "Tasks:\n"
    "1. Resample to **daily** — mean temperature, total rainfall\n"
    "2. Resample to **weekly** — max temperature\n"
    "3. Resample to **monthly** — mean and std of temperature\n"
    "4. Use `asfreq('D')` to get daily frequency (no aggregation) — note the NaNs\n"
    "5. Forward-fill missing values after `asfreq()` and compare with `interpolate()`"
))
cells.append(code(
    "idx = pd.date_range('2024-01-01', periods=60*24, freq='h')\n"
    "np.random.seed(7)\n"
    "sensors = pd.DataFrame({\n"
    "    'temperature': 20 + 10*np.sin(np.linspace(0, 60*2*np.pi/24, len(idx))) + np.random.normal(0, 2, len(idx)),\n"
    "    'rainfall':    np.random.exponential(0.5, len(idx)).round(2),\n"
    "}, index=idx)\n"
    "print(sensors.head(3))\n\n"
    "# 1. Daily mean temp, total rainfall\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Weekly max temperature\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Monthly mean + std of temperature\n"
    "# YOUR CODE HERE\n\n"
    "# 4. asfreq('D') on daily data (use daily resampled from task 1)\n"
    "# YOUR CODE HERE\n\n"
    "# 5. ffill vs interpolate on a sparse daily series\n"
    "sparse = sensors['temperature'].resample('D').mean()\n"
    "sparse_missing = sparse.copy()\n"
    "sparse_missing.iloc[3:6] = np.nan   # introduce gaps\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 22 — crosstab() & Contingency Tables
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 22 — crosstab() & Contingency Tables\n\n"
    "**Scenario:** HR analysis — explore promotion rates across department and gender.\n\n"
    "Tasks:\n"
    "1. Build a crosstab of `dept` vs `promoted` (counts)\n"
    "2. Normalise by row to get promotion **rate** per department\n"
    "3. Add row and column **margins** (totals)\n"
    "4. Build a crosstab of `dept` vs `gender` with `promoted` as the **values** and `mean` as aggfunc\n"
    "5. Find the department with the highest female promotion rate"
))
cells.append(code(
    "np.random.seed(21)\n"
    "n = 1000\n"
    "hr = pd.DataFrame({\n"
    "    'employee_id': range(n),\n"
    "    'dept':     np.random.choice(['Eng','Sales','HR','Finance','Ops'], n),\n"
    "    'gender':   np.random.choice(['M','F'], n, p=[0.55, 0.45]),\n"
    "    'level':    np.random.choice(['Junior','Mid','Senior'], n, p=[0.4,0.4,0.2]),\n"
    "    'promoted': np.random.choice([0, 1], n, p=[0.75, 0.25]),\n"
    "})\n\n"
    "# 1. Basic crosstab\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Row-normalised (promotion rate per dept)\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Add margins\n"
    "# YOUR CODE HERE\n\n"
    "# 4. crosstab dept x gender, values=promoted, aggfunc=mean\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Dept with highest female promotion rate\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 23 — Custom Aggregation with agg()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 23 — Custom Aggregation with agg()\n\n"
    "**Scenario:** Compute rich summary statistics for a sales dataset in one pass.\n\n"
    "Tasks:\n"
    "1. Group by `region` and use a **dict agg** to compute: `revenue` → sum, mean, max; `quantity` → sum, mean\n"
    "2. Use **named aggregations** (pandas ≥ 0.25) to get flat column names\n"
    "3. Write a custom function `iqr(s)` returning the interquartile range and apply it via `agg`\n"
    "4. Apply multiple custom + built-in functions to `revenue` using a list in `agg`\n"
    "5. Use `agg` with a lambda to compute coefficient of variation (`std/mean*100`) per region"
))
cells.append(code(
    "np.random.seed(11)\n"
    "n = 2000\n"
    "sales = pd.DataFrame({\n"
    "    'region':   np.random.choice(['North','South','East','West'], n),\n"
    "    'product':  np.random.choice(['A','B','C','D'], n),\n"
    "    'revenue':  np.random.exponential(500, n).round(2),\n"
    "    'quantity': np.random.randint(1, 50, n),\n"
    "    'discount': np.random.uniform(0, 0.4, n).round(3),\n"
    "})\n\n"
    "# 1. Dict agg\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Named aggregation (no MultiIndex columns)\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Custom IQR function\n"
    "def iqr(s):\n"
    "    return s.quantile(0.75) - s.quantile(0.25)\n"
    "# YOUR CODE HERE\n\n"
    "# 4. List of functions applied to revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Coefficient of variation\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 24 — where() & mask()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 24 — where() & mask() — Conditional Updates\n\n"
    "**Scenario:** Apply business rules to clean and cap sensor and financial data.\n\n"
    "Tasks:\n"
    "1. Use `where()` to keep values only where `temperature` is between -10 and 50, else set to `NaN`\n"
    "2. Use `mask()` to replace `revenue` values below 0 with 0\n"
    "3. Use `where()` to cap `revenue` at the 99th percentile\n"
    "4. Use `np.where()` to create a `price_tier` column: `'high'` if price > 100, else `'low'`\n"
    "5. Chain two `mask()` calls to clean both outlier ends of a distribution"
))
cells.append(code(
    "np.random.seed(24)\n"
    "n = 500\n"
    "df = pd.DataFrame({\n"
    "    'temperature': np.random.normal(20, 30, n).round(1),   # some outliers\n"
    "    'revenue':     np.random.normal(500, 200, n).round(2), # some negatives\n"
    "    'price':       np.random.uniform(10, 200, n).round(2),\n"
    "})\n"
    "print('Revenue negatives before:', (df['revenue'] < 0).sum())\n"
    "print('Temp outliers before:', ((df['temperature'] < -10) | (df['temperature'] > 50)).sum())\n\n"
    "# 1. where() on temperature\n"
    "# YOUR CODE HERE\n\n"
    "# 2. mask() on revenue < 0 → 0\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Cap revenue at 99th percentile\n"
    "# YOUR CODE HERE\n\n"
    "# 4. price_tier using np.where\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Chain mask: remove bottom 1% and top 1% of revenue\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 25 — merge() with indicator & many-to-many
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 25 — merge() with indicator & Many-to-Many\n\n"
    "**Scenario:** Analyse customer orders and tag associations.\n\n"
    "Tasks:\n"
    "1. Left-join `orders` with `customers` on `customer_id`, add `indicator=True`\n"
    "2. Use the `_merge` column to find orders with no matching customer record\n"
    "3. Perform a many-to-many join: merge `products` with `product_tags` (each product can have many tags)\n"
    "4. After the many-to-many join, count products per tag\n"
    "5. Use `validate='many_to_one'` on a join that should be many-to-one — catch the error if it isn't"
))
cells.append(code(
    "np.random.seed(25)\n"
    "customers = pd.DataFrame({\n"
    "    'customer_id': range(1, 101),\n"
    "    'name':  [f'Customer_{i}' for i in range(1, 101)],\n"
    "    'tier':  np.random.choice(['bronze','silver','gold'], 100),\n"
    "})\n"
    "orders = pd.DataFrame({\n"
    "    'order_id':    range(1, 201),\n"
    "    'customer_id': np.random.choice(range(1, 115), 200),  # some IDs > 100 = no match\n"
    "    'amount':      np.random.uniform(20, 500, 200).round(2),\n"
    "})\n"
    "products = pd.DataFrame({'product_id': [1,2,3,4,5], 'name': ['Pen','Notebook','Bag','Lamp','Desk']})\n"
    "product_tags = pd.DataFrame({\n"
    "    'product_id': [1,1,2,2,3,3,4,5,5],\n"
    "    'tag':        ['office','writing','office','paper','travel','storage','lighting','furniture','office'],\n"
    "})\n\n"
    "# 1. Left join with indicator\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Orders with no customer\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Many-to-many: products x product_tags\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Count products per tag\n"
    "# YOUR CODE HERE\n\n"
    "# 5. validate many_to_one (will raise if orders has duplicate customer IDs... use customers join)\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 26 — wide_to_long()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 26 — pd.wide_to_long()\n\n"
    "**Scenario:** Survey data has repeated column patterns (score_2021, score_2022, rank_2021, rank_2022).\n\n"
    "Tasks:\n"
    "1. Use `pd.wide_to_long()` to unpivot columns named `score_YYYY` and `rank_YYYY` into long format\n"
    "2. The result should have columns: `student_id`, `name`, `year`, `score`, `rank`\n"
    "3. Sort by `student_id`, then `year`\n"
    "4. Compute each student's average score across years\n"
    "5. Find students who improved their score from 2021 to 2023"
))
cells.append(code(
    "np.random.seed(26)\n"
    "n = 50\n"
    "students = pd.DataFrame({\n"
    "    'student_id': range(1, n+1),\n"
    "    'name': [f'Student_{i}' for i in range(1, n+1)],\n"
    "    'score_2021': np.random.randint(50, 100, n),\n"
    "    'score_2022': np.random.randint(50, 100, n),\n"
    "    'score_2023': np.random.randint(50, 100, n),\n"
    "    'rank_2021':  np.random.randint(1, n+1, n),\n"
    "    'rank_2022':  np.random.randint(1, n+1, n),\n"
    "    'rank_2023':  np.random.randint(1, n+1, n),\n"
    "})\n"
    "print('Wide shape:', students.shape)\n"
    "print(students.head(2))\n\n"
    "# 1 & 2. wide_to_long\n"
    "# Hint: stubnames=['score','rank'], i=['student_id','name'], j='year', sep='_'\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Sort\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Average score per student\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Students who improved 2021 → 2023\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 27 — Advanced String Operations
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 27 — Advanced String Operations\n\n"
    "**Scenario:** Parse and extract structured data from messy raw text fields.\n\n"
    "Tasks:\n"
    "1. Use `.str.extract()` to pull the **area code** from phone numbers like `(212) 555-1234`\n"
    "2. Use `.str.findall()` to extract all **hashtags** from tweet text\n"
    "3. Use `.str.replace()` with a regex to normalise whitespace (multiple spaces → single space)\n"
    "4. Use `.str.split(expand=True)` to split `full_address` into `street`, `city`, `state`\n"
    "5. Count the number of words in each `bio` field using `.str.count()`"
))
cells.append(code(
    "contacts = pd.DataFrame({\n"
    "    'name':  ['Alice Smith', 'Bob Jones', 'Carol Lee', 'Dave Brown', 'Eve Taylor'],\n"
    "    'phone': ['(212) 555-1234', '(415) 555-9876', '(312) 555-4567', '(646) 555-0011', '(310) 555-7788'],\n"
    "    'tweet': [\n"
    "        'Loving #pandas and #python today!',\n"
    "        '#datascience is the future #ai',\n"
    "        'No hashtags here.',\n"
    "        '#machinelearning #deeplearning rocks',\n"
    "        'Check out #pandas #numpy #scipy',\n"
    "    ],\n"
    "    'full_address': [\n"
    "        '123 Main St, New York, NY',\n"
    "        '456 Oak Ave, San Francisco, CA',\n"
    "        '789 Pine Rd, Chicago, IL',\n"
    "        '321 Elm St, Brooklyn, NY',\n"
    "        '654 Maple Dr, Los Angeles, CA',\n"
    "    ],\n"
    "    'bio': [\n"
    "        'Data  scientist  at  BigCorp',\n"
    "        'ML   engineer and blogger',\n"
    "        'Software developer',\n"
    "        'Analyst at   TechFirm  Inc',\n"
    "        'Researcher  and  writer',\n"
    "    ],\n"
    "})\n\n"
    "# 1. Extract area code\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Extract all hashtags\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Normalise whitespace in bio\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Split full_address\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Word count in bio\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 28 — DateTime Advanced
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 28 — DateTime Advanced\n\n"
    "**Scenario:** Process global trading data with time zones and business day calendars.\n\n"
    "Tasks:\n"
    "1. Localise a naive UTC timestamp column using `dt.tz_localize('UTC')`\n"
    "2. Convert to `'US/Eastern'` timezone using `dt.tz_convert()`\n"
    "3. Generate a date range of the next **10 business days** from today using `pd.bdate_range()`\n"
    "4. Use `pd.offsets.BusinessDay(n)` to add 5 business days to each trade date\n"
    "5. Compute the number of business days between `open_date` and `close_date` using `np.busday_count`"
))
cells.append(code(
    "import pytz\n\n"
    "np.random.seed(28)\n"
    "n = 100\n"
    "base = pd.Timestamp('2024-01-01 09:30:00')\n"
    "trades = pd.DataFrame({\n"
    "    'trade_id':  range(1, n+1),\n"
    "    'timestamp_utc': [base + pd.Timedelta(minutes=np.random.randint(0, 60*8)) for _ in range(n)],\n"
    "    'open_date':  pd.to_datetime(np.random.choice(\n"
    "        pd.date_range('2024-01-01', periods=60).astype(str), n)),\n"
    "    'close_date': pd.to_datetime(np.random.choice(\n"
    "        pd.date_range('2024-03-01', periods=60).astype(str), n)),\n"
    "    'amount':     np.random.uniform(1000, 50000, n).round(2),\n"
    "})\n"
    "print(trades.head(3))\n\n"
    "# 1. Localize timestamp_utc\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Convert to US/Eastern\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Next 10 business days from 2024-01-01\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Add 5 business days to open_date\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Business days between open_date and close_date\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 29 — Chunked CSV Processing
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 29 — Chunked CSV Processing\n\n"
    "**Scenario:** Process a large CSV that doesn't fit in memory by reading it in chunks.\n\n"
    "Tasks:\n"
    "1. Write a 200K-row CSV to disk using pandas (simulate a large file)\n"
    "2. Read it back in chunks of 10K rows using `chunksize`\n"
    "3. For each chunk, compute total revenue per `region` — accumulate results\n"
    "4. Combine all chunk results and get the final total revenue per region\n"
    "5. Verify the chunked result matches reading the whole file at once"
))
cells.append(code(
    "import os, tempfile\n\n"
    "np.random.seed(29)\n"
    "n = 200_000\n"
    "big_df = pd.DataFrame({\n"
    "    'order_id': range(n),\n"
    "    'region':   np.random.choice(['North','South','East','West'], n),\n"
    "    'product':  np.random.choice(['A','B','C'], n),\n"
    "    'revenue':  np.random.exponential(100, n).round(2),\n"
    "    'qty':      np.random.randint(1, 20, n),\n"
    "})\n"
    "tmp_path = os.path.join(tempfile.gettempdir(), 'big_sales.csv')\n"
    "big_df.to_csv(tmp_path, index=False)\n"
    "print(f'Wrote {n:,} rows to {tmp_path}')\n\n"
    "# 2 & 3. Read in chunks and accumulate\n"
    "# YOUR CODE HERE\n"
    "# chunks = []\n"
    "# for chunk in pd.read_csv(tmp_path, chunksize=10_000):\n"
    "#     ...\n\n"
    "# 4. Combine\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Verify\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 30 — Rolling & Expanding Advanced
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 30 — Rolling & Expanding Window Functions (Advanced)\n\n"
    "**Scenario:** Build technical indicators for a stock price series.\n\n"
    "Tasks:\n"
    "1. Compute a **20-day Simple Moving Average (SMA)** of the close price\n"
    "2. Compute a **20-day Exponential Moving Average (EMA)** using `ewm(span=20)`\n"
    "3. Compute **Bollinger Bands**: upper = SMA + 2*std, lower = SMA - 2*std (20-day window)\n"
    "4. Compute **RSI (simplified)**: 14-day average gain / (avg gain + avg loss) * 100\n"
    "5. Use `expanding()` to compute the all-time cumulative max (running peak) of the close price"
))
cells.append(code(
    "np.random.seed(30)\n"
    "n = 252  # ~1 trading year\n"
    "price = pd.DataFrame({'date': pd.bdate_range('2024-01-01', periods=n)})\n"
    "price['close'] = 100 * np.exp(np.cumsum(np.random.normal(0.0005, 0.015, n)))\n"
    "price = price.set_index('date')\n"
    "print(price.head())\n\n"
    "# 1. 20-day SMA\n"
    "# YOUR CODE HERE\n\n"
    "# 2. 20-day EMA\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Bollinger Bands\n"
    "# YOUR CODE HERE\n\n"
    "# 4. RSI (14-day)\n"
    "delta = price['close'].diff()\n"
    "# YOUR CODE HERE — compute gain, loss, RSI\n\n"
    "# 5. Expanding cumulative max (all-time high)\n"
    "# YOUR CODE HERE\n\n"
    "print(price[['close','sma20','ema20','bb_upper','bb_lower','rsi14','all_time_high']].tail())"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 31 — groupby + transform
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 31 — groupby + transform (Broadcast Aggregation)\n\n"
    "**Scenario:** Enrich each row with group-level statistics without losing any rows.\n\n"
    "Tasks:\n"
    "1. Add `dept_avg_salary` — the average salary for each employee's department (same shape as original)\n"
    "2. Add `dept_rank` — rank of each employee's salary within their department\n"
    "3. Add `salary_vs_dept_avg` — how much above/below the dept average each employee is (%)\n"
    "4. Add `dept_headcount` — number of employees in each department\n"
    "5. Flag employees whose salary is in the top 25% of their department"
))
cells.append(code(
    "np.random.seed(31)\n"
    "n = 500\n"
    "employees = pd.DataFrame({\n"
    "    'emp_id': range(1, n+1),\n"
    "    'dept':   np.random.choice(['Eng','Sales','HR','Finance','Ops'], n),\n"
    "    'level':  np.random.choice(['Junior','Mid','Senior'], n, p=[0.4,0.4,0.2]),\n"
    "    'salary': np.random.normal(70000, 20000, n).clip(30000, 200000).round(-2),\n"
    "})\n"
    "print(employees.head())\n\n"
    "# 1. dept_avg_salary via transform\n"
    "# YOUR CODE HERE\n\n"
    "# 2. dept_rank (1 = highest salary in dept)\n"
    "# YOUR CODE HERE\n\n"
    "# 3. salary_vs_dept_avg %\n"
    "# YOUR CODE HERE\n\n"
    "# 4. dept_headcount\n"
    "# YOUR CODE HERE\n\n"
    "# 5. top 25% flag within dept\n"
    "# YOUR CODE HERE\n\n"
    "print(employees[['emp_id','dept','salary','dept_avg_salary','dept_rank','top25_flag']].head(10))"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 32 — apply() axis=1 vs vectorized
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 32 — apply(axis=1) vs Vectorized Operations\n\n"
    "**Scenario:** Compute shipping costs using complex business rules, then optimize.\n\n"
    "Tasks:\n"
    "1. Write a function `calc_shipping(row)` that returns shipping cost based on `weight`, `distance`, and `zone`\n"
    "   - zone A: base 5 + 0.01 * distance + 0.5 * weight\n"
    "   - zone B: base 8 + 0.015 * distance + 0.7 * weight\n"
    "   - zone C: base 12 + 0.02 * distance + 1.0 * weight\n"
    "2. Apply it with `apply(axis=1)` and time it\n"
    "3. Implement the same logic using **vectorized** `np.select()` and time it\n"
    "4. Verify both approaches produce identical results\n"
    "5. Compute the speedup ratio"
))
cells.append(code(
    "import time\n"
    "np.random.seed(32)\n"
    "n = 50_000\n"
    "shipments = pd.DataFrame({\n"
    "    'order_id': range(n),\n"
    "    'weight':   np.random.uniform(0.1, 30, n).round(2),\n"
    "    'distance': np.random.randint(10, 2000, n),\n"
    "    'zone':     np.random.choice(['A','B','C'], n),\n"
    "})\n\n"
    "# 1 & 2. apply(axis=1)\n"
    "def calc_shipping(row):\n"
    "    if row['zone'] == 'A':\n"
    "        return 5 + 0.01 * row['distance'] + 0.5 * row['weight']\n"
    "    elif row['zone'] == 'B':\n"
    "        return 8 + 0.015 * row['distance'] + 0.7 * row['weight']\n"
    "    else:\n"
    "        return 12 + 0.02 * row['distance'] + 1.0 * row['weight']\n\n"
    "t0 = time.time()\n"
    "shipments['cost_apply'] = shipments.apply(calc_shipping, axis=1)\n"
    "t_apply = time.time() - t0\n"
    "print(f'apply: {t_apply:.3f}s')\n\n"
    "# 3. Vectorized with np.select\n"
    "t0 = time.time()\n"
    "# YOUR CODE HERE\n"
    "t_vec = time.time() - t0\n"
    "print(f'vectorized: {t_vec:.3f}s')\n\n"
    "# 4 & 5. Verify + speedup\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 33 — Hierarchical GroupBy
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 33 — Hierarchical GroupBy (Multiple Levels)\n\n"
    "**Scenario:** Drill down through country → region → city in an e-commerce dataset.\n\n"
    "Tasks:\n"
    "1. GroupBy `['country', 'region']` → sum revenue\n"
    "2. GroupBy `['country', 'region', 'city']` → count orders and mean order value\n"
    "3. Use `unstack()` on a two-level groupby result to create a pivot-like view\n"
    "4. Find the **best city** (highest total revenue) per country\n"
    "5. Compute revenue as a **percentage of its country total** using `groupby + transform`"
))
cells.append(code(
    "np.random.seed(33)\n"
    "n = 3000\n"
    "geo = pd.DataFrame({\n"
    "    'order_id':    range(n),\n"
    "    'country':     np.random.choice(['US','UK','DE'], n, p=[0.5,0.3,0.2]),\n"
    "    'region':      np.random.choice(['North','South','East','West'], n),\n"
    "    'city':        np.random.choice(['CityA','CityB','CityC','CityD'], n),\n"
    "    'category':    np.random.choice(['Electronics','Clothing','Food'], n),\n"
    "    'revenue':     np.random.exponential(150, n).round(2),\n"
    "    'order_value': np.random.uniform(20, 500, n).round(2),\n"
    "})\n\n"
    "# 1. Country + Region → revenue sum\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Country + Region + City → order count + mean order value\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Unstack category level to see wide view (country x category)\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Best city per country by total revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Revenue % of country total per row\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 34 — merge_asof()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 34 — merge_asof() — Time-Based Join\n\n"
    "**Scenario:** Join trade execution data with the most recent bid/ask quote.\n\n"
    "Tasks:\n"
    "1. Use `pd.merge_asof()` to join each `trade` with the most recent `quote` at or before the trade time\n"
    "2. Compute the **spread** at trade time: `ask - bid`\n"
    "3. Check whether each trade was executed at the bid, ask, or in-between\n"
    "4. Try `direction='forward'` to get the next quote after each trade instead\n"
    "5. Count how many trades had no prior quote available (result is NaN)"
))
cells.append(code(
    "np.random.seed(34)\n"
    "quote_times = pd.date_range('2024-01-15 09:30:00', periods=100, freq='30s')\n"
    "quotes = pd.DataFrame({\n"
    "    'time': quote_times,\n"
    "    'bid':  (150 + np.cumsum(np.random.normal(0, 0.05, 100))).round(3),\n"
    "})\n"
    "quotes['ask'] = (quotes['bid'] + np.random.uniform(0.01, 0.05, 100)).round(3)\n\n"
    "trade_times = pd.date_range('2024-01-15 09:30:00', periods=30, freq='90s')\n"
    "trades = pd.DataFrame({\n"
    "    'time':  trade_times,\n"
    "    'price': (150 + np.cumsum(np.random.normal(0, 0.05, 30))).round(3),\n"
    "    'size':  np.random.randint(100, 1000, 30),\n"
    "})\n"
    "# Both must be sorted by 'time'\n"
    "quotes = quotes.sort_values('time')\n"
    "trades = trades.sort_values('time')\n\n"
    "# 1. merge_asof (backward = default)\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Spread at trade time\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Classify trade vs quote\n"
    "# YOUR CODE HERE\n\n"
    "# 4. direction='forward'\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Count NaN bid rows\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 35 — pivot_table() with margins & aggfunc
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 35 — pivot_table() with margins & Multiple aggfunc\n\n"
    "**Scenario:** Build an executive summary table of sales across channels and regions.\n\n"
    "Tasks:\n"
    "1. Create a pivot table: rows=`region`, columns=`channel`, values=`revenue`, aggfunc=`sum`\n"
    "2. Add `margins=True` to get row and column totals\n"
    "3. Create a pivot with **two aggfuncs**: `{'revenue': ['sum','mean'], 'units': 'sum'}`\n"
    "4. Fill missing combinations with 0 using `fill_value=0`\n"
    "5. Use `observed=True` with a categorical column to suppress empty categories"
))
cells.append(code(
    "np.random.seed(35)\n"
    "n = 2000\n"
    "sales = pd.DataFrame({\n"
    "    'region':  np.random.choice(['North','South','East','West'], n),\n"
    "    'channel': np.random.choice(['Online','Retail','Wholesale'], n, p=[0.5,0.3,0.2]),\n"
    "    'product': np.random.choice(['A','B','C','D'], n),\n"
    "    'revenue': np.random.exponential(300, n).round(2),\n"
    "    'units':   np.random.randint(1, 50, n),\n"
    "})\n\n"
    "# 1. Basic pivot\n"
    "# YOUR CODE HERE\n\n"
    "# 2. With margins\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Multiple aggfuncs\n"
    "# YOUR CODE HERE\n\n"
    "# 4. fill_value=0\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Categorical + observed=True\n"
    "sales['channel_cat'] = pd.Categorical(sales['channel'],\n"
    "    categories=['Online','Retail','Wholesale','Direct'], ordered=False)\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 36 — DataFrame.compare()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 36 — DataFrame.compare()\n\n"
    "**Scenario:** Audit changes made to a customer database between two versions.\n\n"
    "Tasks:\n"
    "1. Use `df1.compare(df2)` to find all cells that changed\n"
    "2. Use `result_names=('before', 'after')` for clearer column labels\n"
    "3. Count how many rows changed (have at least one difference)\n"
    "4. Find which columns had the most changes\n"
    "5. Extract only the rows where `email` changed"
))
cells.append(code(
    "np.random.seed(36)\n"
    "n = 100\n"
    "base = pd.DataFrame({\n"
    "    'customer_id': range(1, n+1),\n"
    "    'name':   [f'Customer_{i}' for i in range(1, n+1)],\n"
    "    'email':  [f'user{i}@email.com' for i in range(1, n+1)],\n"
    "    'score':  np.random.randint(1, 100, n),\n"
    "    'tier':   np.random.choice(['free','paid','premium'], n),\n"
    "}).set_index('customer_id')\n\n"
    "# Simulate some changes\n"
    "updated = base.copy()\n"
    "idx_score  = np.random.choice(n, 15, replace=False)\n"
    "idx_tier   = np.random.choice(n, 10, replace=False)\n"
    "idx_email  = np.random.choice(n, 5,  replace=False)\n"
    "updated.iloc[idx_score, updated.columns.get_loc('score')] += 10\n"
    "updated.iloc[idx_tier,  updated.columns.get_loc('tier')]  = 'premium'\n"
    "for i in idx_email:\n"
    "    updated.iloc[i, updated.columns.get_loc('email')] = f'new{i}@updated.com'\n\n"
    "# 1. compare\n"
    "# YOUR CODE HERE\n\n"
    "# 2. result_names\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Count changed rows\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Changes per column\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Rows where email changed\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 37 — pd.json_normalize()
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 37 — pd.json_normalize() — Flatten Nested JSON\n\n"
    "**Scenario:** API response returns deeply nested JSON. Flatten it for analysis.\n\n"
    "Tasks:\n"
    "1. Use `pd.json_normalize()` to flatten a list of nested user records\n"
    "2. Rename columns to replace dots with underscores for easier access\n"
    "3. Flatten the nested `orders` list within each record using `record_path`\n"
    "4. Set `max_level=1` to partially flatten (only one level deep)\n"
    "5. Compute total order value per user from the flattened data"
))
cells.append(code(
    "import json\n\n"
    "raw_data = [\n"
    "    {'id': 1, 'name': 'Alice', 'address': {'city': 'NYC', 'country': 'US'},\n"
    "     'profile': {'age': 30, 'tier': 'gold'},\n"
    "     'orders': [{'oid': 101, 'value': 250.0}, {'oid': 102, 'value': 80.0}]},\n"
    "    {'id': 2, 'name': 'Bob',   'address': {'city': 'LA',  'country': 'US'},\n"
    "     'profile': {'age': 25, 'tier': 'silver'},\n"
    "     'orders': [{'oid': 103, 'value': 120.0}]},\n"
    "    {'id': 3, 'name': 'Carol', 'address': {'city': 'London', 'country': 'UK'},\n"
    "     'profile': {'age': 35, 'tier': 'bronze'},\n"
    "     'orders': [{'oid': 104, 'value': 330.0}, {'oid': 105, 'value': 60.0}, {'oid': 106, 'value': 90.0}]},\n"
    "]\n\n"
    "# 1. Basic json_normalize\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Rename dots → underscores\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Flatten orders using record_path\n"
    "# YOUR CODE HERE\n\n"
    "# 4. max_level=1\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Total order value per user\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 38 — IntervalIndex & pd.cut advanced
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 38 — IntervalIndex & pd.cut Advanced\n\n"
    "**Scenario:** Build custom price bands for a retail product catalogue.\n\n"
    "Tasks:\n"
    "1. Use `pd.cut()` with custom bins and labels to create `price_band`\n"
    "2. Use `pd.IntervalIndex.from_tuples()` to create a custom index for lookup\n"
    "3. Map each product's price to a discount tier using the IntervalIndex\n"
    "4. Use `pd.qcut()` to split prices into equal-frequency quintiles (5 groups)\n"
    "5. Compare the distribution of products across `cut` bands vs `qcut` quintiles"
))
cells.append(code(
    "np.random.seed(38)\n"
    "n = 500\n"
    "products = pd.DataFrame({\n"
    "    'product_id': range(1, n+1),\n"
    "    'category':   np.random.choice(['Electronics','Clothing','Food','Sports'], n),\n"
    "    'price':      np.random.lognormal(4, 1, n).round(2).clip(1, 2000),\n"
    "})\n"
    "print(products['price'].describe())\n\n"
    "# 1. Custom cut with labels\n"
    "bins   = [0, 25, 50, 100, 250, 500, np.inf]\n"
    "labels = ['budget','economy','mid','upper-mid','premium','luxury']\n"
    "# YOUR CODE HERE\n\n"
    "# 2. IntervalIndex for discount tiers\n"
    "intervals = pd.IntervalIndex.from_tuples([(0,25),(25,100),(100,500),(500,np.inf)], closed='left')\n"
    "discount_tiers = pd.Series([20, 15, 10, 5], index=intervals, name='discount_pct')\n"
    "# YOUR CODE HERE — map each product to its discount\n\n"
    "# 3. Already done via IntervalIndex lookup — verify\n"
    "print(products[['price','price_band','discount_pct']].head(10))\n\n"
    "# 4. qcut into 5 quintiles\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Compare distributions\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 39 — GroupBy + Cumulative Stats
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 39 — GroupBy + Cumulative Statistics\n\n"
    "**Scenario:** Track running performance metrics for each sales rep over time.\n\n"
    "Tasks:\n"
    "1. Compute `cumsum` of `revenue` per `rep_id` (running total per rep)\n"
    "2. Compute `cummax` of `revenue` per rep (personal best)\n"
    "3. Compute `cumprod` of daily `growth_rate` per rep (compound growth)\n"
    "4. Compute the **cumulative rank** of each rep's daily revenue within their group\n"
    "5. Compute a **30-day rolling average** within each rep group using `groupby + rolling`"
))
cells.append(code(
    "np.random.seed(39)\n"
    "n_reps = 5\n"
    "n_days = 90\n"
    "rep_ids   = [f'REP{i:02d}' for i in range(1, n_reps+1)]\n"
    "dates     = pd.date_range('2024-01-01', periods=n_days, freq='D')\n"
    "idx       = pd.MultiIndex.from_product([rep_ids, dates], names=['rep_id','date'])\n"
    "perf = pd.DataFrame({\n"
    "    'revenue':     np.random.exponential(1000, len(idx)).round(2),\n"
    "    'growth_rate': np.random.uniform(0.98, 1.04, len(idx)).round(4),\n"
    "}, index=idx).reset_index()\n"
    "print(perf.head())\n\n"
    "# 1. Cumulative revenue per rep\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Personal best revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Compound growth\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Cumulative rank within group\n"
    "# YOUR CODE HERE\n\n"
    "# 5. 30-day rolling avg within rep group\n"
    "# YOUR CODE HERE\n\n"
    "print(perf.tail(10))"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 40 — Mini Project: End-to-End Sales Pipeline
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 40 — Mini Project: End-to-End Sales Pipeline\n\n"
    "**Scenario:** Build a complete ETL + analysis pipeline for a multi-channel e-commerce company.\n\n"
    "**Step 1 — Ingest & Validate:**\n"
    "- Load orders, customers, and products tables\n"
    "- Check for duplicates, nulls, and data type issues\n\n"
    "**Step 2 — Clean & Enrich:**\n"
    "- Merge all three tables\n"
    "- Add `revenue = price * quantity * (1 - discount)`\n"
    "- Add `age_group` and `customer_tier` columns\n\n"
    "**Step 3 — Analyse:**\n"
    "- Monthly revenue trend (with MoM %)\n"
    "- Top 5 products by total revenue\n"
    "- Revenue breakdown by channel and region\n"
    "- Customer cohort: first-purchase month vs LTV\n\n"
    "**Step 4 — Summarise:**\n"
    "- Print an executive summary: total revenue, orders, AOV, top region, top product\n"
    "- Export the enriched DataFrame to CSV"
))
cells.append(code(
    "from datetime import timedelta\n"
    "import os, tempfile\n\n"
    "np.random.seed(40)\n"
    "N_CUSTOMERS = 2000\n"
    "N_PRODUCTS  = 50\n"
    "N_ORDERS    = 15000\n\n"
    "# ── Raw Tables ──────────────────────────────────────────────\n"
    "customers_df = pd.DataFrame({\n"
    "    'customer_id': range(1, N_CUSTOMERS+1),\n"
    "    'name':        [f'Customer_{i}' for i in range(1, N_CUSTOMERS+1)],\n"
    "    'age':         np.random.randint(18, 75, N_CUSTOMERS),\n"
    "    'gender':      np.random.choice(['M','F'], N_CUSTOMERS),\n"
    "    'region':      np.random.choice(['North','South','East','West'], N_CUSTOMERS),\n"
    "    'channel':     np.random.choice(['Online','Retail','Mobile'], N_CUSTOMERS, p=[0.5,0.3,0.2]),\n"
    "})\n\n"
    "products_df = pd.DataFrame({\n"
    "    'product_id':  range(1, N_PRODUCTS+1),\n"
    "    'product_name':[f'Product_{i}' for i in range(1, N_PRODUCTS+1)],\n"
    "    'category':    np.random.choice(['Electronics','Clothing','Food','Sports','Home'], N_PRODUCTS),\n"
    "    'price':       np.random.uniform(5, 500, N_PRODUCTS).round(2),\n"
    "})\n\n"
    "orders_df = pd.DataFrame({\n"
    "    'order_id':    range(1, N_ORDERS+1),\n"
    "    'customer_id': np.random.randint(1, N_CUSTOMERS+1, N_ORDERS),\n"
    "    'product_id':  np.random.randint(1, N_PRODUCTS+1, N_ORDERS),\n"
    "    'order_date':  pd.to_datetime(np.random.choice(\n"
    "        pd.date_range('2023-01-01','2024-12-31').astype(str), N_ORDERS)),\n"
    "    'quantity':    np.random.randint(1, 10, N_ORDERS),\n"
    "    'discount':    np.random.choice([0, 0.05, 0.10, 0.15, 0.20], N_ORDERS, p=[0.5,0.2,0.15,0.1,0.05]),\n"
    "})\n\n"
    "# ── Step 1: Validate ────────────────────────────────────────\n"
    "# Check for duplicates and nulls in each table\n"
    "# YOUR CODE HERE\n\n"
    "# ── Step 2: Clean & Enrich ──────────────────────────────────\n"
    "# Merge orders with customers and products\n"
    "# Add revenue = price * quantity * (1 - discount)\n"
    "# Add age_group using pd.cut\n"
    "# YOUR CODE HERE\n\n"
    "# ── Step 3: Analyse ─────────────────────────────────────────\n"
    "# 3a. Monthly revenue + MoM %\n"
    "# YOUR CODE HERE\n\n"
    "# 3b. Top 5 products by revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 3c. Revenue by channel and region (pivot)\n"
    "# YOUR CODE HERE\n\n"
    "# 3d. First-purchase cohort: cohort month vs avg LTV\n"
    "# YOUR CODE HERE\n\n"
    "# ── Step 4: Executive Summary ───────────────────────────────\n"
    "# YOUR CODE HERE\n\n"
    "# Export enriched df to CSV\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# SOLUTIONS
# ══════════════════════════════════════════════════════════════════════════
cells.append(md("---\n# ✅ Solutions (21–40)\n\n> Try first!"))

# Sol 21
cells.append(md("## Solution 21 — Time Series Resampling"))
cells.append(code(
    "idx = pd.date_range('2024-01-01', periods=60*24, freq='h')\n"
    "np.random.seed(7)\n"
    "sensors = pd.DataFrame({\n"
    "    'temperature': 20 + 10*np.sin(np.linspace(0, 60*2*np.pi/24, len(idx))) + np.random.normal(0, 2, len(idx)),\n"
    "    'rainfall':    np.random.exponential(0.5, len(idx)).round(2),\n"
    "}, index=idx)\n\n"
    "daily = sensors.resample('D').agg({'temperature': 'mean', 'rainfall': 'sum'})\n"
    "print('Daily (head):'); print(daily.head())\n\n"
    "weekly_max = sensors['temperature'].resample('W').max()\n"
    "print('Weekly max temp (head):'); print(weekly_max.head())\n\n"
    "monthly = sensors['temperature'].resample('ME').agg(['mean','std']).round(2)\n"
    "print('Monthly stats:'); print(monthly)\n\n"
    "daily_freq = daily['temperature'].asfreq('D')\n"
    "print('NaN count after asfreq:', daily_freq.isna().sum())  # should be 0 here\n\n"
    "sparse = sensors['temperature'].resample('D').mean()\n"
    "sparse_missing = sparse.copy(); sparse_missing.iloc[3:6] = np.nan\n"
    "ffill_result = sparse_missing.ffill()\n"
    "interp_result = sparse_missing.interpolate(method='linear')\n"
    "print('ffill vs interpolate at gap:'); print(pd.concat([sparse_missing, ffill_result, interp_result], axis=1, keys=['original','ffill','interp']).iloc[2:8])"
))

# Sol 22
cells.append(md("## Solution 22 — crosstab()"))
cells.append(code(
    "np.random.seed(21)\n"
    "n = 1000\n"
    "hr = pd.DataFrame({'employee_id':range(n),'dept':np.random.choice(['Eng','Sales','HR','Finance','Ops'],n),'gender':np.random.choice(['M','F'],n,p=[0.55,0.45]),'level':np.random.choice(['Junior','Mid','Senior'],n,p=[0.4,0.4,0.2]),'promoted':np.random.choice([0,1],n,p=[0.75,0.25])})\n\n"
    "ct = pd.crosstab(hr['dept'], hr['promoted'])\n"
    "print(ct)\n\n"
    "ct_norm = pd.crosstab(hr['dept'], hr['promoted'], normalize='index').round(3)\n"
    "print(ct_norm)\n\n"
    "ct_margins = pd.crosstab(hr['dept'], hr['promoted'], margins=True)\n"
    "print(ct_margins)\n\n"
    "ct_val = pd.crosstab(hr['dept'], hr['gender'], values=hr['promoted'], aggfunc='mean').round(3)\n"
    "print(ct_val)\n\n"
    "best_female_dept = ct_val['F'].idxmax()\n"
    "print('Best dept for female promotion:', best_female_dept)"
))

# Sol 23
cells.append(md("## Solution 23 — Custom Aggregation"))
cells.append(code(
    "np.random.seed(11)\n"
    "n = 2000\n"
    "sales = pd.DataFrame({'region':np.random.choice(['North','South','East','West'],n),'product':np.random.choice(['A','B','C','D'],n),'revenue':np.random.exponential(500,n).round(2),'quantity':np.random.randint(1,50,n),'discount':np.random.uniform(0,0.4,n).round(3)})\n\n"
    "r1 = sales.groupby('region').agg({'revenue':['sum','mean','max'],'quantity':['sum','mean']})\n"
    "print(r1)\n\n"
    "r2 = sales.groupby('region').agg(\n"
    "    rev_total=('revenue','sum'), rev_mean=('revenue','mean'), rev_max=('revenue','max'),\n"
    "    qty_total=('quantity','sum'), qty_mean=('quantity','mean')\n"
    ").round(2)\n"
    "print(r2)\n\n"
    "def iqr(s): return s.quantile(0.75) - s.quantile(0.25)\n"
    "print(sales.groupby('region')['revenue'].agg(iqr).round(2))\n\n"
    "print(sales.groupby('region')['revenue'].agg(['sum','mean','std', iqr]).round(2))\n\n"
    "cv = sales.groupby('region')['revenue'].agg(lambda s: s.std()/s.mean()*100).round(2)\n"
    "print('Coefficient of variation:'); print(cv)"
))

# Sol 24
cells.append(md("## Solution 24 — where() & mask()"))
cells.append(code(
    "np.random.seed(24)\n"
    "n = 500\n"
    "df = pd.DataFrame({'temperature':np.random.normal(20,30,n).round(1),'revenue':np.random.normal(500,200,n).round(2),'price':np.random.uniform(10,200,n).round(2)})\n\n"
    "df['temp_clean'] = df['temperature'].where((df['temperature'] >= -10) & (df['temperature'] <= 50))\n"
    "print('Temp NaNs after where:', df['temp_clean'].isna().sum())\n\n"
    "df['revenue_clean'] = df['revenue'].mask(df['revenue'] < 0, 0)\n"
    "print('Revenue negatives after mask:', (df['revenue_clean'] < 0).sum())\n\n"
    "cap99 = df['revenue'].quantile(0.99)\n"
    "df['revenue_capped'] = df['revenue'].where(df['revenue'] <= cap99, cap99)\n"
    "print(f'Capped at {cap99:.2f} — max now: {df[\"revenue_capped\"].max():.2f}')\n\n"
    "df['price_tier'] = np.where(df['price'] > 100, 'high', 'low')\n"
    "print(df['price_tier'].value_counts())\n\n"
    "p1, p99 = df['revenue'].quantile(0.01), df['revenue'].quantile(0.99)\n"
    "df['rev_trimmed'] = df['revenue'].mask(df['revenue'] < p1).mask(df['revenue'] > p99)\n"
    "print('Trimmed NaN count:', df['rev_trimmed'].isna().sum())"
))

# Sol 25
cells.append(md("## Solution 25 — merge() indicator & many-to-many"))
cells.append(code(
    "np.random.seed(25)\n"
    "customers = pd.DataFrame({'customer_id':range(1,101),'name':[f'Customer_{i}' for i in range(1,101)],'tier':np.random.choice(['bronze','silver','gold'],100)})\n"
    "orders = pd.DataFrame({'order_id':range(1,201),'customer_id':np.random.choice(range(1,115),200),'amount':np.random.uniform(20,500,200).round(2)})\n"
    "products = pd.DataFrame({'product_id':[1,2,3,4,5],'name':['Pen','Notebook','Bag','Lamp','Desk']})\n"
    "product_tags = pd.DataFrame({'product_id':[1,1,2,2,3,3,4,5,5],'tag':['office','writing','office','paper','travel','storage','lighting','furniture','office']})\n\n"
    "merged = orders.merge(customers, on='customer_id', how='left', indicator=True)\n"
    "print('_merge counts:'); print(merged['_merge'].value_counts())\n\n"
    "no_cust = merged[merged['_merge'] == 'left_only']\n"
    "print('Orders with no customer:', len(no_cust))\n\n"
    "prod_tagged = products.merge(product_tags, on='product_id')\n"
    "print(prod_tagged)\n\n"
    "tag_counts = prod_tagged.groupby('tag')['product_id'].count().sort_values(ascending=False)\n"
    "print(tag_counts)\n\n"
    "try:\n"
    "    orders.merge(customers, on='customer_id', how='inner', validate='many_to_one')\n"
    "    print('Validation passed')\n"
    "except Exception as e:\n"
    "    print('Validation error:', e)"
))

# Sol 26
cells.append(md("## Solution 26 — wide_to_long()"))
cells.append(code(
    "np.random.seed(26)\n"
    "n = 50\n"
    "students = pd.DataFrame({'student_id':range(1,n+1),'name':[f'Student_{i}' for i in range(1,n+1)],'score_2021':np.random.randint(50,100,n),'score_2022':np.random.randint(50,100,n),'score_2023':np.random.randint(50,100,n),'rank_2021':np.random.randint(1,n+1,n),'rank_2022':np.random.randint(1,n+1,n),'rank_2023':np.random.randint(1,n+1,n)})\n\n"
    "long = pd.wide_to_long(students, stubnames=['score','rank'], i=['student_id','name'], j='year', sep='_')\n"
    "long = long.reset_index().sort_values(['student_id','year'])\n"
    "print('Long shape:', long.shape); print(long.head(6))\n\n"
    "avg_score = long.groupby('student_id')['score'].mean().round(2)\n"
    "print(avg_score.head())\n\n"
    "pivot_s = long.pivot(index='student_id', columns='year', values='score')\n"
    "improved = pivot_s[pivot_s[2023] > pivot_s[2021]]\n"
    "print(f'Students who improved 2021->2023: {len(improved)}')"
))

# Sol 27
cells.append(md("## Solution 27 — Advanced String Ops"))
cells.append(code(
    "contacts = pd.DataFrame({'name':['Alice Smith','Bob Jones','Carol Lee','Dave Brown','Eve Taylor'],'phone':['(212) 555-1234','(415) 555-9876','(312) 555-4567','(646) 555-0011','(310) 555-7788'],'tweet':['Loving #pandas and #python today!','#datascience is the future #ai','No hashtags here.','#machinelearning #deeplearning rocks','Check out #pandas #numpy #scipy'],'full_address':['123 Main St, New York, NY','456 Oak Ave, San Francisco, CA','789 Pine Rd, Chicago, IL','321 Elm St, Brooklyn, NY','654 Maple Dr, Los Angeles, CA'],'bio':['Data  scientist  at  BigCorp','ML   engineer and blogger','Software developer','Analyst at   TechFirm  Inc','Researcher  and  writer']})\n\n"
    "contacts['area_code'] = contacts['phone'].str.extract(r'\\((\\d{3})\\)')\n"
    "print(contacts[['name','area_code']])\n\n"
    "contacts['hashtags'] = contacts['tweet'].str.findall(r'#\\w+')\n"
    "print(contacts[['name','hashtags']])\n\n"
    "contacts['bio_clean'] = contacts['bio'].str.replace(r'\\s+', ' ', regex=True).str.strip()\n"
    "print(contacts[['bio','bio_clean']])\n\n"
    "addr_split = contacts['full_address'].str.split(', ', expand=True)\n"
    "addr_split.columns = ['street','city','state']\n"
    "print(addr_split)\n\n"
    "contacts['word_count'] = contacts['bio_clean'].str.count(r'\\S+')\n"
    "print(contacts[['name','word_count']])"
))

# Sol 28
cells.append(md("## Solution 28 — DateTime Advanced"))
cells.append(code(
    "import pytz\n"
    "np.random.seed(28)\n"
    "n = 100\n"
    "base = pd.Timestamp('2024-01-15 09:30:00')\n"
    "trades = pd.DataFrame({'trade_id':range(1,n+1),'timestamp_utc':[base+pd.Timedelta(minutes=int(x)) for x in np.random.randint(0,60*8,n)],'open_date':pd.to_datetime(np.random.choice(pd.date_range('2024-01-01',periods=60).astype(str),n)),'close_date':pd.to_datetime(np.random.choice(pd.date_range('2024-03-01',periods=60).astype(str),n)),'amount':np.random.uniform(1000,50000,n).round(2)})\n\n"
    "trades['ts_utc'] = trades['timestamp_utc'].dt.tz_localize('UTC')\n"
    "print(trades['ts_utc'].head(2))\n\n"
    "trades['ts_eastern'] = trades['ts_utc'].dt.tz_convert('US/Eastern')\n"
    "print(trades['ts_eastern'].head(2))\n\n"
    "bdays = pd.bdate_range('2024-01-01', periods=10)\n"
    "print('Next 10 business days:', bdays.tolist())\n\n"
    "trades['settlement'] = trades['open_date'] + pd.offsets.BusinessDay(5)\n"
    "print(trades[['open_date','settlement']].head())\n\n"
    "od = trades['open_date'].dt.date.astype(str).values\n"
    "cd = trades['close_date'].dt.date.astype(str).values\n"
    "trades['bdays_open'] = np.busday_count(od, cd)\n"
    "print(trades[['open_date','close_date','bdays_open']].head())"
))

# Sol 29
cells.append(md("## Solution 29 — Chunked CSV Processing"))
cells.append(code(
    "import os, tempfile\n"
    "np.random.seed(29)\n"
    "n = 200_000\n"
    "big_df = pd.DataFrame({'order_id':range(n),'region':np.random.choice(['North','South','East','West'],n),'product':np.random.choice(['A','B','C'],n),'revenue':np.random.exponential(100,n).round(2),'qty':np.random.randint(1,20,n)})\n"
    "tmp_path = os.path.join(tempfile.gettempdir(), 'big_sales.csv')\n"
    "big_df.to_csv(tmp_path, index=False)\n\n"
    "chunks = []\n"
    "for chunk in pd.read_csv(tmp_path, chunksize=10_000):\n"
    "    chunks.append(chunk.groupby('region')['revenue'].sum())\n\n"
    "chunked_result = pd.concat(chunks).groupby(level=0).sum().round(2)\n"
    "print('Chunked result:'); print(chunked_result)\n\n"
    "full_result = big_df.groupby('region')['revenue'].sum().round(2)\n"
    "print('Full result:');    print(full_result)\n"
    "print('Match:', chunked_result.equals(full_result))"
))

# Sol 30
cells.append(md("## Solution 30 — Rolling & Expanding Advanced"))
cells.append(code(
    "np.random.seed(30)\n"
    "n = 252\n"
    "price = pd.DataFrame({'close': 100 * np.exp(np.cumsum(np.random.normal(0.0005, 0.015, n)))},\n"
    "                     index=pd.bdate_range('2024-01-01', periods=n))\n\n"
    "price['sma20'] = price['close'].rolling(20).mean()\n"
    "price['ema20'] = price['close'].ewm(span=20, adjust=False).mean()\n\n"
    "std20 = price['close'].rolling(20).std()\n"
    "price['bb_upper'] = price['sma20'] + 2 * std20\n"
    "price['bb_lower'] = price['sma20'] - 2 * std20\n\n"
    "delta = price['close'].diff()\n"
    "gain  = delta.clip(lower=0)\n"
    "loss  = (-delta).clip(lower=0)\n"
    "avg_gain = gain.rolling(14).mean()\n"
    "avg_loss = loss.rolling(14).mean()\n"
    "rs = avg_gain / avg_loss\n"
    "price['rsi14'] = (100 - (100 / (1 + rs))).round(2)\n\n"
    "price['all_time_high'] = price['close'].expanding().max()\n"
    "print(price[['close','sma20','ema20','bb_upper','bb_lower','rsi14','all_time_high']].tail())"
))

# Sol 31
cells.append(md("## Solution 31 — groupby + transform"))
cells.append(code(
    "np.random.seed(31)\n"
    "n = 500\n"
    "employees = pd.DataFrame({'emp_id':range(1,n+1),'dept':np.random.choice(['Eng','Sales','HR','Finance','Ops'],n),'level':np.random.choice(['Junior','Mid','Senior'],n,p=[0.4,0.4,0.2]),'salary':np.random.normal(70000,20000,n).clip(30000,200000).round(-2)})\n\n"
    "employees['dept_avg_salary'] = employees.groupby('dept')['salary'].transform('mean').round(2)\n"
    "employees['dept_rank'] = employees.groupby('dept')['salary'].rank(ascending=False, method='min').astype(int)\n"
    "employees['salary_vs_dept_avg'] = ((employees['salary'] - employees['dept_avg_salary']) / employees['dept_avg_salary'] * 100).round(2)\n"
    "employees['dept_headcount'] = employees.groupby('dept')['emp_id'].transform('count')\n"
    "q75 = employees.groupby('dept')['salary'].transform(lambda x: x.quantile(0.75))\n"
    "employees['top25_flag'] = employees['salary'] >= q75\n"
    "print(employees[['emp_id','dept','salary','dept_avg_salary','dept_rank','top25_flag']].head(10))"
))

# Sol 32
cells.append(md("## Solution 32 — apply(axis=1) vs vectorized"))
cells.append(code(
    "import time\n"
    "np.random.seed(32)\n"
    "n = 50_000\n"
    "shipments = pd.DataFrame({'order_id':range(n),'weight':np.random.uniform(0.1,30,n).round(2),'distance':np.random.randint(10,2000,n),'zone':np.random.choice(['A','B','C'],n)})\n\n"
    "def calc_shipping(row):\n"
    "    if row['zone']=='A': return 5  + 0.01 *row['distance'] + 0.5*row['weight']\n"
    "    elif row['zone']=='B': return 8 + 0.015*row['distance'] + 0.7*row['weight']\n"
    "    else: return 12 + 0.02*row['distance'] + 1.0*row['weight']\n\n"
    "t0 = time.time()\n"
    "shipments['cost_apply'] = shipments.apply(calc_shipping, axis=1)\n"
    "t_apply = time.time() - t0\n"
    "print(f'apply: {t_apply:.3f}s')\n\n"
    "t0 = time.time()\n"
    "conds = [shipments['zone']=='A', shipments['zone']=='B', shipments['zone']=='C']\n"
    "choices = [\n"
    "    5  + 0.01 *shipments['distance'] + 0.5*shipments['weight'],\n"
    "    8  + 0.015*shipments['distance'] + 0.7*shipments['weight'],\n"
    "    12 + 0.02 *shipments['distance'] + 1.0*shipments['weight'],\n"
    "]\n"
    "shipments['cost_vec'] = np.select(conds, choices)\n"
    "t_vec = time.time() - t0\n"
    "print(f'vectorized: {t_vec:.3f}s')\n\n"
    "match = np.allclose(shipments['cost_apply'], shipments['cost_vec'])\n"
    "print(f'Results match: {match} | Speedup: {t_apply/t_vec:.1f}x')"
))

# Sol 33
cells.append(md("## Solution 33 — Hierarchical GroupBy"))
cells.append(code(
    "np.random.seed(33)\n"
    "n = 3000\n"
    "geo = pd.DataFrame({'order_id':range(n),'country':np.random.choice(['US','UK','DE'],n,p=[0.5,0.3,0.2]),'region':np.random.choice(['North','South','East','West'],n),'city':np.random.choice(['CityA','CityB','CityC','CityD'],n),'category':np.random.choice(['Electronics','Clothing','Food'],n),'revenue':np.random.exponential(150,n).round(2),'order_value':np.random.uniform(20,500,n).round(2)})\n\n"
    "r1 = geo.groupby(['country','region'])['revenue'].sum().round(2)\n"
    "print(r1.head(8))\n\n"
    "r2 = geo.groupby(['country','region','city']).agg(orders=('order_id','count'), mean_val=('order_value','mean')).round(2)\n"
    "print(r2.head(6))\n\n"
    "cat_pivot = geo.groupby(['country','category'])['revenue'].sum().unstack(fill_value=0).round(0)\n"
    "print(cat_pivot)\n\n"
    "city_rev = geo.groupby(['country','city'])['revenue'].sum()\n"
    "best_city = city_rev.groupby(level='country').idxmax().apply(lambda x: x[1])\n"
    "print('Best city per country:', best_city)\n\n"
    "geo['country_total'] = geo.groupby('country')['revenue'].transform('sum')\n"
    "geo['rev_pct'] = (geo['revenue'] / geo['country_total'] * 100).round(4)\n"
    "print(geo[['country','revenue','rev_pct']].head())"
))

# Sol 34
cells.append(md("## Solution 34 — merge_asof()"))
cells.append(code(
    "np.random.seed(34)\n"
    "quote_times = pd.date_range('2024-01-15 09:30:00', periods=100, freq='30s')\n"
    "quotes = pd.DataFrame({'time':quote_times,'bid':(150+np.cumsum(np.random.normal(0,0.05,100))).round(3)})\n"
    "quotes['ask'] = (quotes['bid']+np.random.uniform(0.01,0.05,100)).round(3)\n"
    "trade_times = pd.date_range('2024-01-15 09:30:00', periods=30, freq='90s')\n"
    "trades = pd.DataFrame({'time':trade_times,'price':(150+np.cumsum(np.random.normal(0,0.05,30))).round(3),'size':np.random.randint(100,1000,30)})\n"
    "quotes = quotes.sort_values('time'); trades = trades.sort_values('time')\n\n"
    "joined = pd.merge_asof(trades, quotes, on='time', direction='backward')\n"
    "print(joined.head())\n\n"
    "joined['spread'] = (joined['ask'] - joined['bid']).round(4)\n"
    "print('Avg spread at trade time:', joined['spread'].mean().round(4))\n\n"
    "joined['side'] = np.where(joined['price'] >= joined['ask'], 'buy',\n"
    "                  np.where(joined['price'] <= joined['bid'], 'sell', 'mid'))\n"
    "print(joined['side'].value_counts())\n\n"
    "fwd = pd.merge_asof(trades, quotes, on='time', direction='forward')\n"
    "print('Forward join NaN bid:', fwd['bid'].isna().sum())\n\n"
    "print('No prior quote:', joined['bid'].isna().sum())"
))

# Sol 35
cells.append(md("## Solution 35 — pivot_table() advanced"))
cells.append(code(
    "np.random.seed(35)\n"
    "n = 2000\n"
    "sales = pd.DataFrame({'region':np.random.choice(['North','South','East','West'],n),'channel':np.random.choice(['Online','Retail','Wholesale'],n,p=[0.5,0.3,0.2]),'product':np.random.choice(['A','B','C','D'],n),'revenue':np.random.exponential(300,n).round(2),'units':np.random.randint(1,50,n)})\n\n"
    "pt1 = pd.pivot_table(sales, values='revenue', index='region', columns='channel', aggfunc='sum')\n"
    "print(pt1.round(0))\n\n"
    "pt2 = pd.pivot_table(sales, values='revenue', index='region', columns='channel', aggfunc='sum', margins=True)\n"
    "print(pt2.round(0))\n\n"
    "pt3 = pd.pivot_table(sales, values={'revenue':['sum','mean'],'units':'sum'}, index='region', columns='channel')\n"
    "print(pt3.round(0))\n\n"
    "pt4 = pd.pivot_table(sales, values='revenue', index='region', columns='channel', aggfunc='sum', fill_value=0)\n"
    "print(pt4.round(0))\n\n"
    "sales['channel_cat'] = pd.Categorical(sales['channel'], categories=['Online','Retail','Wholesale','Direct'], ordered=False)\n"
    "pt5 = pd.pivot_table(sales, values='revenue', index='region', columns='channel_cat', aggfunc='sum', fill_value=0, observed=True)\n"
    "print(pt5.round(0))  # 'Direct' column excluded"
))

# Sol 36
cells.append(md("## Solution 36 — DataFrame.compare()"))
cells.append(code(
    "np.random.seed(36)\n"
    "n = 100\n"
    "base = pd.DataFrame({'customer_id':range(1,n+1),'name':[f'Customer_{i}' for i in range(1,n+1)],'email':[f'user{i}@email.com' for i in range(1,n+1)],'score':np.random.randint(1,100,n),'tier':np.random.choice(['free','paid','premium'],n)}).set_index('customer_id')\n"
    "updated = base.copy()\n"
    "idx_score=np.random.choice(n,15,replace=False); idx_tier=np.random.choice(n,10,replace=False); idx_email=np.random.choice(n,5,replace=False)\n"
    "updated.iloc[idx_score, updated.columns.get_loc('score')] += 10\n"
    "updated.iloc[idx_tier,  updated.columns.get_loc('tier')]  = 'premium'\n"
    "for i in idx_email: updated.iloc[i, updated.columns.get_loc('email')] = f'new{i}@updated.com'\n\n"
    "diff = base.compare(updated)\n"
    "print('Changed cells shape:', diff.shape)\n\n"
    "diff2 = base.compare(updated, result_names=('before','after'))\n"
    "print(diff2.head())\n\n"
    "changed_rows = diff.index\n"
    "print('Changed row count:', len(changed_rows))\n\n"
    "changes_per_col = diff.notna().any(axis=1).groupby(level=0).sum() if diff.columns.nlevels > 1 else None\n"
    "col_change_count = diff.notna().sum().groupby(level=0).sum()\n"
    "print('Changes per column:'); print(col_change_count)\n\n"
    "email_diff = diff2[diff2['email'].notna().any(axis=1)] if 'email' in diff2.columns.get_level_values(0) else 'no email changes'\n"
    "print('Email changes:'); print(email_diff)"
))

# Sol 37
cells.append(md("## Solution 37 — pd.json_normalize()"))
cells.append(code(
    "raw_data = [{'id':1,'name':'Alice','address':{'city':'NYC','country':'US'},'profile':{'age':30,'tier':'gold'},'orders':[{'oid':101,'value':250.0},{'oid':102,'value':80.0}]},{'id':2,'name':'Bob','address':{'city':'LA','country':'US'},'profile':{'age':25,'tier':'silver'},'orders':[{'oid':103,'value':120.0}]},{'id':3,'name':'Carol','address':{'city':'London','country':'UK'},'profile':{'age':35,'tier':'bronze'},'orders':[{'oid':104,'value':330.0},{'oid':105,'value':60.0},{'oid':106,'value':90.0}]}]\n\n"
    "flat = pd.json_normalize(raw_data)\n"
    "print('Columns:', flat.columns.tolist())\n"
    "print(flat[['id','name','address.city','profile.tier']])\n\n"
    "flat.columns = flat.columns.str.replace('.', '_', regex=False)\n"
    "print('Renamed:', flat.columns.tolist())\n\n"
    "orders_flat = pd.json_normalize(raw_data, record_path='orders', meta=['id','name'])\n"
    "print(orders_flat)\n\n"
    "partial = pd.json_normalize(raw_data, max_level=1)\n"
    "print('max_level=1 cols:', partial.columns.tolist())\n\n"
    "total_per_user = orders_flat.groupby('id')['value'].sum()\n"
    "print('Total order value per user:'); print(total_per_user)"
))

# Sol 38
cells.append(md("## Solution 38 — IntervalIndex & pd.cut"))
cells.append(code(
    "np.random.seed(38)\n"
    "n = 500\n"
    "products = pd.DataFrame({'product_id':range(1,n+1),'category':np.random.choice(['Electronics','Clothing','Food','Sports'],n),'price':np.random.lognormal(4,1,n).round(2).clip(1,2000)})\n\n"
    "bins = [0,25,50,100,250,500,np.inf]\n"
    "labels = ['budget','economy','mid','upper-mid','premium','luxury']\n"
    "products['price_band'] = pd.cut(products['price'], bins=bins, labels=labels)\n"
    "print(products['price_band'].value_counts().sort_index())\n\n"
    "intervals = pd.IntervalIndex.from_tuples([(0,25),(25,100),(100,500),(500,np.inf)], closed='left')\n"
    "discount_tiers = pd.Series([20,15,10,5], index=intervals, name='discount_pct')\n"
    "products['discount_pct'] = pd.cut(products['price'], bins=intervals).map(discount_tiers)\n"
    "print(products[['price','price_band','discount_pct']].head(10))\n\n"
    "products['price_quintile'] = pd.qcut(products['price'], q=5, labels=['Q1','Q2','Q3','Q4','Q5'])\n"
    "print('qcut quintiles:'); print(products['price_quintile'].value_counts().sort_index())\n\n"
    "comp = pd.crosstab(products['price_band'], products['price_quintile'])\n"
    "print('cut vs qcut distribution:'); print(comp)"
))

# Sol 39
cells.append(md("## Solution 39 — GroupBy + Cumulative Stats"))
cells.append(code(
    "np.random.seed(39)\n"
    "n_reps=5; n_days=90\n"
    "rep_ids=[f'REP{i:02d}' for i in range(1,n_reps+1)]\n"
    "dates=pd.date_range('2024-01-01',periods=n_days,freq='D')\n"
    "idx=pd.MultiIndex.from_product([rep_ids,dates],names=['rep_id','date'])\n"
    "perf=pd.DataFrame({'revenue':np.random.exponential(1000,len(idx)).round(2),'growth_rate':np.random.uniform(0.98,1.04,len(idx)).round(4)},index=idx).reset_index()\n"
    "perf = perf.sort_values(['rep_id','date'])\n\n"
    "perf['cum_revenue']   = perf.groupby('rep_id')['revenue'].cumsum()\n"
    "perf['personal_best'] = perf.groupby('rep_id')['revenue'].cummax()\n"
    "perf['compound_growth'] = perf.groupby('rep_id')['growth_rate'].cumprod()\n"
    "perf['cum_rank'] = perf.groupby(['rep_id','date'])['revenue'].rank(pct=True)\n"
    "perf['rolling_avg_30'] = (\n"
    "    perf.groupby('rep_id')['revenue']\n"
    "        .transform(lambda x: x.rolling(30, min_periods=1).mean())\n"
    ").round(2)\n"
    "print(perf.tail(10))"
))

# Sol 40
cells.append(md("## Solution 40 — End-to-End Sales Pipeline"))
cells.append(code(
    "import os, tempfile\n"
    "np.random.seed(40)\n"
    "N_CUSTOMERS=2000; N_PRODUCTS=50; N_ORDERS=15000\n\n"
    "customers_df = pd.DataFrame({'customer_id':range(1,N_CUSTOMERS+1),'name':[f'Customer_{i}' for i in range(1,N_CUSTOMERS+1)],'age':np.random.randint(18,75,N_CUSTOMERS),'gender':np.random.choice(['M','F'],N_CUSTOMERS),'region':np.random.choice(['North','South','East','West'],N_CUSTOMERS),'channel':np.random.choice(['Online','Retail','Mobile'],N_CUSTOMERS,p=[0.5,0.3,0.2])})\n"
    "products_df = pd.DataFrame({'product_id':range(1,N_PRODUCTS+1),'product_name':[f'Product_{i}' for i in range(1,N_PRODUCTS+1)],'category':np.random.choice(['Electronics','Clothing','Food','Sports','Home'],N_PRODUCTS),'price':np.random.uniform(5,500,N_PRODUCTS).round(2)})\n"
    "orders_df = pd.DataFrame({'order_id':range(1,N_ORDERS+1),'customer_id':np.random.randint(1,N_CUSTOMERS+1,N_ORDERS),'product_id':np.random.randint(1,N_PRODUCTS+1,N_ORDERS),'order_date':pd.to_datetime(np.random.choice(pd.date_range('2023-01-01','2024-12-31').astype(str),N_ORDERS)),'quantity':np.random.randint(1,10,N_ORDERS),'discount':np.random.choice([0,0.05,0.10,0.15,0.20],N_ORDERS,p=[0.5,0.2,0.15,0.1,0.05])})\n\n"
    "# Step 1: Validate\n"
    "for name, df in [('customers',customers_df),('products',products_df),('orders',orders_df)]:\n"
    "    print(f'{name}: {len(df)} rows | dups={df.duplicated().sum()} | nulls={df.isna().sum().sum()}')\n\n"
    "# Step 2: Merge & enrich\n"
    "enriched = (\n"
    "    orders_df\n"
    "    .merge(customers_df, on='customer_id', how='left')\n"
    "    .merge(products_df,  on='product_id',  how='left')\n"
    "    .assign(\n"
    "        revenue   = lambda d: (d['price'] * d['quantity'] * (1 - d['discount'])).round(2),\n"
    "        age_group = lambda d: pd.cut(d['age'], bins=[17,30,45,65,100], labels=['18-30','31-45','46-65','65+']),\n"
    "        year_month = lambda d: d['order_date'].dt.to_period('M'),\n"
    "    )\n"
    ")\n"
    "print('Enriched shape:', enriched.shape)\n\n"
    "# Step 3a: Monthly revenue + MoM\n"
    "monthly = enriched.groupby('year_month')['revenue'].sum().reset_index()\n"
    "monthly['mom_pct'] = monthly['revenue'].pct_change().mul(100).round(2)\n"
    "print(monthly.tail(6).to_string(index=False))\n\n"
    "# Step 3b: Top 5 products\n"
    "top5 = enriched.groupby('product_name')['revenue'].sum().nlargest(5)\n"
    "print('Top 5 products:'); print(top5.round(0))\n\n"
    "# Step 3c: Channel x Region pivot\n"
    "ch_reg = pd.pivot_table(enriched, values='revenue', index='region', columns='channel', aggfunc='sum', fill_value=0).round(0)\n"
    "print(ch_reg)\n\n"
    "# Step 3d: Cohort LTV\n"
    "first_purchase = enriched.groupby('customer_id')['order_date'].min().dt.to_period('M').rename('cohort')\n"
    "cohort_ltv = enriched.merge(first_purchase, on='customer_id').groupby('cohort')['revenue'].mean().round(2)\n"
    "print('Avg LTV by cohort (first 6):'); print(cohort_ltv.head(6))\n\n"
    "# Step 4: Executive summary\n"
    "print('\\n── EXECUTIVE SUMMARY ──')\n"
    "print(f'Total Revenue:  ${enriched[\"revenue\"].sum():,.0f}')\n"
    "print(f'Total Orders:   {len(orders_df):,}')\n"
    "print(f'Avg Order Value: ${enriched[\"revenue\"].mean():.2f}')\n"
    "print(f'Top Region:     {enriched.groupby(\"region\")[\"revenue\"].sum().idxmax()}')\n"
    "print(f'Top Product:    {enriched.groupby(\"product_name\")[\"revenue\"].sum().idxmax()}')\n\n"
    "out = os.path.join(tempfile.gettempdir(), 'enriched_sales.csv')\n"
    "enriched.to_csv(out, index=False)\n"
    "print(f'Exported to {out}')"
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

path = os.path.join(OUT, "pandas_practice_expert.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

size_kb = os.path.getsize(path) / 1024
print(f"Created: {path}")
print(f"  {len(cells)} cells | {size_kb:.1f} KB")
print(f"  20 expert exercises + 20 solutions")
