import json, os

OUT = r"c:\Users\seany\Documents\All Codes\Python Panda Library Study"

def md(src): return {"cell_type":"markdown","metadata":{},"source":[src]}
def code(src): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[src]}

cells = []

# ── Title ────────────────────────────────────────────────────────────────
cells.append(md(
    "# 🐼 Pandas Practice Exercises\n\n"
    "**10 real-world challenges** covering the most important pandas skills.\n\n"
    "Each exercise has:\n"
    "- A problem description with sample data\n"
    "- Starter code with `# YOUR CODE HERE` markers\n"
    "- A solution cell at the bottom (scroll down or try first!)\n\n"
    "---"
))

# ── Setup ─────────────────────────────────────────────────────────────────
cells.append(md("## Setup"))
cells.append(code(
    "import pandas as pd\n"
    "import numpy as np\n"
    "np.random.seed(42)\n"
    "print('pandas:', pd.__version__)"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 1
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 1 — Sales Data Inspection\n\n"
    "**Scenario:** You're given a sales DataFrame. Answer these questions:\n"
    "1. How many rows and columns?\n"
    "2. What are the data types of each column?\n"
    "3. Are there any missing values?\n"
    "4. What is the total revenue?\n"
    "5. Show the top 3 rows sorted by `revenue` descending."
))
cells.append(code(
    "sales = pd.DataFrame({\n"
    "    'product': ['Widget A','Widget B','Widget C','Widget A','Widget B',None,'Widget C','Widget A'],\n"
    "    'region':  ['North','South','East','West','North','South','East','West'],\n"
    "    'units':   [120, 85, 200, 60, 150, 95, None, 180],\n"
    "    'price':   [9.99, 14.99, 4.99, 9.99, 14.99, 4.99, 4.99, 9.99],\n"
    "})\n"
    "sales['revenue'] = sales['units'] * sales['price']\n\n"
    "# 1. Shape\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Data types\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Missing values\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Total revenue (skip NaN)\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Top 3 by revenue\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 2
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 2 — Data Cleaning\n\n"
    "**Scenario:** A messy customer export needs cleaning before analysis.\n\n"
    "Tasks:\n"
    "1. Strip leading/trailing whitespace from `name` and `email`\n"
    "2. Convert `signup_date` to datetime\n"
    "3. Fill missing `age` with the median age\n"
    "4. Drop duplicate rows (keep first)\n"
    "5. Reset the index after dropping"
))
cells.append(code(
    "customers = pd.DataFrame({\n"
    "    'name':        ['  Alice ', 'Bob', '  Carol', 'Dave', 'Bob'],\n"
    "    'email':       ['alice@x.com ', 'bob@x.com', 'carol@x.com', ' dave@x.com', 'bob@x.com'],\n"
    "    'age':         [28, None, 34, 41, None],\n"
    "    'signup_date': ['2023-01-15', '2023-03-22', '2023-06-01', '2022-11-30', '2023-03-22'],\n"
    "})\n\n"
    "# 1. Strip whitespace\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Convert signup_date to datetime\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Fill missing age with median\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Drop duplicates\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Reset index\n"
    "# YOUR CODE HERE\n\n"
    "print(customers)"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 3
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 3 — GroupBy & Aggregation\n\n"
    "**Scenario:** Analyse employee salaries by department and seniority.\n\n"
    "Tasks:\n"
    "1. Average salary per `dept`\n"
    "2. For each `dept`: count employees, min salary, max salary, total salary\n"
    "3. Which dept has the highest average salary?\n"
    "4. Add a column `salary_rank` ranking each employee within their dept (1 = highest)"
))
cells.append(code(
    "employees = pd.DataFrame({\n"
    "    'name':   ['Alice','Bob','Carol','Dave','Eve','Frank','Grace','Hank','Ivy'],\n"
    "    'dept':   ['Eng','Eng','Sales','Sales','HR','HR','Eng','Sales','HR'],\n"
    "    'level':  ['Senior','Junior','Senior','Junior','Senior','Junior','Mid','Mid','Junior'],\n"
    "    'salary': [120000,75000,95000,65000,70000,55000,90000,72000,60000],\n"
    "})\n\n"
    "# 1. Average salary per dept\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Multi-agg per dept\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Highest avg salary dept\n"
    "# YOUR CODE HERE\n\n"
    "# 4. salary_rank within dept (1 = highest)\n"
    "# YOUR CODE HERE\n\n"
    "print(employees[['name','dept','salary','salary_rank']])"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 4
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 4 — Merge & Join\n\n"
    "**Scenario:** Combine orders, customers, and products tables.\n\n"
    "Tasks:\n"
    "1. Inner join `orders` with `customers` on `cust_id`\n"
    "2. Left join the result with `products` on `prod_id`\n"
    "3. Find customers who have **never** placed an order\n"
    "4. Calculate total spend per customer name"
))
cells.append(code(
    "orders = pd.DataFrame({\n"
    "    'order_id': [1,2,3,4,5],\n"
    "    'cust_id':  [101,102,101,103,102],\n"
    "    'prod_id':  ['P1','P2','P3','P1','P2'],\n"
    "    'qty':      [2, 1, 3, 1, 2],\n"
    "})\n"
    "customers = pd.DataFrame({\n"
    "    'cust_id': [101,102,103,104],\n"
    "    'name':    ['Alice','Bob','Carol','Dave'],\n"
    "    'city':    ['NY','LA','NY','Chicago'],\n"
    "})\n"
    "products = pd.DataFrame({\n"
    "    'prod_id': ['P1','P2','P3'],\n"
    "    'name':    ['Widget','Gadget','Doohickey'],\n"
    "    'price':   [9.99, 24.99, 4.99],\n"
    "})\n\n"
    "# 1. Inner join orders + customers\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Left join result + products\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Customers with no orders\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Total spend per customer (qty * price)\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 5
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 5 — String Operations\n\n"
    "**Scenario:** Parse and clean a raw user export from a CRM.\n\n"
    "Tasks:\n"
    "1. Extract the domain from each `email` (part after `@`)\n"
    "2. Split `full_name` into `first_name` and `last_name` columns\n"
    "3. Create a `username` column: lowercase first name + first letter of last name (e.g. `alices`)\n"
    "4. Flag rows where the phone number does NOT match pattern `XXX-XXX-XXXX`\n"
    "5. Count how many users per email domain"
))
cells.append(code(
    "users = pd.DataFrame({\n"
    "    'full_name': ['Alice Smith','Bob Jones','Carol White','Dave Brown','Eve Davis'],\n"
    "    'email':     ['alice@gmail.com','bob@yahoo.com','carol@gmail.com','dave@company.org','eve@yahoo.com'],\n"
    "    'phone':     ['212-555-1234','555-1234','310-555-9876','212-555-4321','(415)555-0000'],\n"
    "})\n\n"
    "# 1. Email domain\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Split name\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Username\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Invalid phone flag (valid = digits-digits-digits like 212-555-1234)\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Users per domain\n"
    "# YOUR CODE HERE\n\n"
    "print(users)"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 6
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 6 — DateTime Operations\n\n"
    "**Scenario:** Analyse a daily website traffic log.\n\n"
    "Tasks:\n"
    "1. Parse `date` column as datetime\n"
    "2. Add columns: `year`, `month`, `day_of_week` (Mon=0)\n"
    "3. Filter for weekdays only (Mon–Fri)\n"
    "4. Find the date with the highest traffic\n"
    "5. Calculate the 7-day rolling average of `visits`"
))
cells.append(code(
    "dates = pd.date_range('2024-01-01', periods=60, freq='D')\n"
    "traffic = pd.DataFrame({\n"
    "    'date':   dates.strftime('%Y-%m-%d'),\n"
    "    'visits': np.random.randint(1000, 10000, 60),\n"
    "    'bounces': np.random.randint(200, 5000, 60),\n"
    "})\n\n"
    "# 1. Parse date\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Add year, month, day_of_week\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Weekdays only\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Date with highest visits\n"
    "# YOUR CODE HERE\n\n"
    "# 5. 7-day rolling average\n"
    "# YOUR CODE HERE\n\n"
    "print(traffic.head(10))"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 7
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 7 — Pivot Tables\n\n"
    "**Scenario:** Build a sales summary report by region and product.\n\n"
    "Tasks:\n"
    "1. Create a pivot table: rows=`region`, columns=`product`, values=`revenue`, aggfunc=`sum`\n"
    "2. Add row/column totals (margins)\n"
    "3. Fill any NaN in the pivot with 0\n"
    "4. Find which region-product combo had the highest single-month revenue\n"
    "5. Use `melt()` to convert the pivot back to long format"
))
cells.append(code(
    "np.random.seed(0)\n"
    "n = 200\n"
    "store_sales = pd.DataFrame({\n"
    "    'month':   np.random.choice(['Jan','Feb','Mar','Apr'], n),\n"
    "    'region':  np.random.choice(['North','South','East','West'], n),\n"
    "    'product': np.random.choice(['Widget','Gadget','Doohickey'], n),\n"
    "    'revenue': np.random.randint(100, 5000, n),\n"
    "})\n\n"
    "# 1. Pivot table\n"
    "# YOUR CODE HERE\n\n"
    "# 2. With margins\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Fill NaN with 0\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Highest single revenue row in original df\n"
    "# YOUR CODE HERE\n\n"
    "# 5. melt pivot back to long\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 8
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 8 — Apply & Custom Functions\n\n"
    "**Scenario:** Score and categorise loan applications.\n\n"
    "Tasks:\n"
    "1. Add `debt_ratio` = `debt / income` (round to 2 dp)\n"
    "2. Add `risk_score`: 0–100 based on `credit_score` (map linearly: 300→0, 850→100)\n"
    "3. Add `risk_category`: `'Low'` if risk_score ≥ 70, `'Medium'` if 40–69, `'High'` if < 40\n"
    "4. Add `approved`: True if `debt_ratio` < 0.4 AND `risk_score` ≥ 60\n"
    "5. Show approval rate per `risk_category`"
))
cells.append(code(
    "np.random.seed(7)\n"
    "n = 300\n"
    "loans = pd.DataFrame({\n"
    "    'applicant_id': range(1, n+1),\n"
    "    'income':       np.random.randint(25000, 150000, n),\n"
    "    'debt':         np.random.randint(5000, 80000, n),\n"
    "    'credit_score': np.random.randint(300, 850, n),\n"
    "})\n\n"
    "# 1. debt_ratio\n"
    "# YOUR CODE HERE\n\n"
    "# 2. risk_score (linear map 300-850 -> 0-100)\n"
    "# YOUR CODE HERE\n\n"
    "# 3. risk_category\n"
    "# YOUR CODE HERE\n\n"
    "# 4. approved\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Approval rate per risk_category\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 9
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 9 — Window Functions & Time Series\n\n"
    "**Scenario:** Analyse a stock price series.\n\n"
    "Tasks:\n"
    "1. Calculate the 5-day and 20-day rolling mean of `close`\n"
    "2. Calculate daily `pct_change` and flag days where change > ±3%\n"
    "3. Calculate cumulative return from day 1 (start = 1.0)\n"
    "4. Find the maximum drawdown: biggest peak-to-trough drop\n"
    "5. Add a `signal` column: `'BUY'` when 5d_ma crosses above 20d_ma, `'SELL'` when it crosses below, else `'HOLD'`"
))
cells.append(code(
    "np.random.seed(42)\n"
    "dates = pd.date_range('2024-01-01', periods=120, freq='B')  # business days\n"
    "returns = np.random.normal(0.0005, 0.015, 120)\n"
    "prices = 100 * np.cumprod(1 + returns)\n"
    "stock = pd.DataFrame({'date': dates, 'close': prices.round(2)})\n"
    "stock = stock.set_index('date')\n\n"
    "# 1. 5d and 20d rolling mean\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Daily pct_change and big_move flag\n"
    "# YOUR CODE HERE\n\n"
    "# 3. Cumulative return\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Maximum drawdown\n"
    "# YOUR CODE HERE (hint: rolling max then (close - rolling_max) / rolling_max)\n\n"
    "# 5. BUY/SELL/HOLD signal\n"
    "# YOUR CODE HERE\n\n"
    "print(stock.tail(10))"
))

# ══════════════════════════════════════════════════════════════════════════
# Exercise 10 — Mini Project
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "## Exercise 10 — Mini Project: E-Commerce Analysis\n\n"
    "**Scenario:** Full end-to-end analysis of an online store's transaction data.\n\n"
    "Tasks:\n"
    "1. Load and inspect the data (shape, dtypes, nulls)\n"
    "2. Clean: parse `order_date`, fill missing `discount` with 0, drop rows with null `customer_id`\n"
    "3. Add `net_revenue` = `quantity * unit_price * (1 - discount)`\n"
    "4. Monthly revenue trend (group by month, sum net_revenue)\n"
    "5. Top 5 customers by total spend\n"
    "6. Category performance: avg order value and total orders per `category`\n"
    "7. Cohort: which month did each customer first order? Add `first_order_month` column\n"
    "8. Flag repeat customers (more than 1 order) vs one-time buyers\n"
    "9. Export a summary DataFrame to CSV (use `StringIO` to avoid writing a file)"
))
cells.append(code(
    "np.random.seed(42)\n"
    "n = 500\n"
    "ecommerce = pd.DataFrame({\n"
    "    'order_id':    range(1001, 1001+n),\n"
    "    'customer_id': np.random.choice([f'C{i:03d}' for i in range(1,81)] + [None], n, p=[1/81]*80 + [1/81]),\n"
    "    'order_date':  pd.date_range('2023-01-01', periods=n, freq='14H').strftime('%Y-%m-%d'),\n"
    "    'category':    np.random.choice(['Electronics','Clothing','Books','Home','Sports'], n),\n"
    "    'quantity':    np.random.randint(1, 6, n),\n"
    "    'unit_price':  np.random.choice([9.99,19.99,49.99,99.99,199.99], n),\n"
    "    'discount':    np.random.choice([0, 0, 0, 0.1, 0.2, None], n),\n"
    "})\n\n"
    "# 1. Inspect\n"
    "# YOUR CODE HERE\n\n"
    "# 2. Clean\n"
    "# YOUR CODE HERE\n\n"
    "# 3. net_revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 4. Monthly revenue\n"
    "# YOUR CODE HERE\n\n"
    "# 5. Top 5 customers\n"
    "# YOUR CODE HERE\n\n"
    "# 6. Category performance\n"
    "# YOUR CODE HERE\n\n"
    "# 7. First order month per customer\n"
    "# YOUR CODE HERE\n\n"
    "# 8. Repeat vs one-time flag\n"
    "# YOUR CODE HERE\n\n"
    "# 9. Export summary to CSV string\n"
    "# from io import StringIO\n"
    "# YOUR CODE HERE"
))

# ══════════════════════════════════════════════════════════════════════════
# SOLUTIONS
# ══════════════════════════════════════════════════════════════════════════
cells.append(md(
    "---\n"
    "# ✅ Solutions\n\n"
    "> Attempt each exercise before peeking!"
))

# Solution 1
cells.append(md("## Solution 1 — Sales Data Inspection"))
cells.append(code(
    "sales = pd.DataFrame({\n"
    "    'product': ['Widget A','Widget B','Widget C','Widget A','Widget B',None,'Widget C','Widget A'],\n"
    "    'region':  ['North','South','East','West','North','South','East','West'],\n"
    "    'units':   [120, 85, 200, 60, 150, 95, None, 180],\n"
    "    'price':   [9.99, 14.99, 4.99, 9.99, 14.99, 4.99, 4.99, 9.99],\n"
    "})\n"
    "sales['revenue'] = sales['units'] * sales['price']\n\n"
    "print('1. Shape:', sales.shape)\n"
    "print('2. Dtypes:')\n"
    "print(sales.dtypes)\n"
    "print('3. Missing values:')\n"
    "print(sales.isnull().sum())\n"
    "print('4. Total revenue:', sales['revenue'].sum())\n"
    "print('5. Top 3 by revenue:')\n"
    "print(sales.nlargest(3, 'revenue'))"
))

# Solution 2
cells.append(md("## Solution 2 — Data Cleaning"))
cells.append(code(
    "customers = pd.DataFrame({\n"
    "    'name':        ['  Alice ', 'Bob', '  Carol', 'Dave', 'Bob'],\n"
    "    'email':       ['alice@x.com ', 'bob@x.com', 'carol@x.com', ' dave@x.com', 'bob@x.com'],\n"
    "    'age':         [28, None, 34, 41, None],\n"
    "    'signup_date': ['2023-01-15', '2023-03-22', '2023-06-01', '2022-11-30', '2023-03-22'],\n"
    "})\n"
    "customers['name'] = customers['name'].str.strip()\n"
    "customers['email'] = customers['email'].str.strip()\n"
    "customers['signup_date'] = pd.to_datetime(customers['signup_date'])\n"
    "customers['age'] = customers['age'].fillna(customers['age'].median())\n"
    "customers = customers.drop_duplicates().reset_index(drop=True)\n"
    "print(customers)"
))

# Solution 3
cells.append(md("## Solution 3 — GroupBy & Aggregation"))
cells.append(code(
    "employees = pd.DataFrame({\n"
    "    'name':   ['Alice','Bob','Carol','Dave','Eve','Frank','Grace','Hank','Ivy'],\n"
    "    'dept':   ['Eng','Eng','Sales','Sales','HR','HR','Eng','Sales','HR'],\n"
    "    'level':  ['Senior','Junior','Senior','Junior','Senior','Junior','Mid','Mid','Junior'],\n"
    "    'salary': [120000,75000,95000,65000,70000,55000,90000,72000,60000],\n"
    "})\n"
    "print('1. Avg salary per dept:')\n"
    "print(employees.groupby('dept')['salary'].mean())\n\n"
    "print('2. Full stats:')\n"
    "print(employees.groupby('dept')['salary'].agg(['count','min','max','sum']))\n\n"
    "best_dept = employees.groupby('dept')['salary'].mean().idxmax()\n"
    "print('3. Highest avg salary dept:', best_dept)\n\n"
    "employees['salary_rank'] = employees.groupby('dept')['salary'].rank(ascending=False, method='min').astype(int)\n"
    "print(employees[['name','dept','salary','salary_rank']])"
))

# Solution 4
cells.append(md("## Solution 4 — Merge & Join"))
cells.append(code(
    "orders = pd.DataFrame({'order_id':[1,2,3,4,5],'cust_id':[101,102,101,103,102],'prod_id':['P1','P2','P3','P1','P2'],'qty':[2,1,3,1,2]})\n"
    "customers = pd.DataFrame({'cust_id':[101,102,103,104],'name':['Alice','Bob','Carol','Dave'],'city':['NY','LA','NY','Chicago']})\n"
    "products = pd.DataFrame({'prod_id':['P1','P2','P3'],'name':['Widget','Gadget','Doohickey'],'price':[9.99,24.99,4.99]})\n\n"
    "merged = orders.merge(customers, on='cust_id', how='inner')\n"
    "merged = merged.merge(products, on='prod_id', how='left', suffixes=('','_product'))\n"
    "print('Merged:')\n"
    "print(merged)\n\n"
    "no_orders = customers[~customers['cust_id'].isin(orders['cust_id'])]\n"
    "print('No orders:', no_orders[['cust_id','name']].to_string(index=False))\n\n"
    "merged['spend'] = merged['qty'] * merged['price']\n"
    "print('Total spend per customer:')\n"
    "print(merged.groupby('name')['spend'].sum().sort_values(ascending=False))"
))

# Solution 5
cells.append(md("## Solution 5 — String Operations"))
cells.append(code(
    "users = pd.DataFrame({\n"
    "    'full_name': ['Alice Smith','Bob Jones','Carol White','Dave Brown','Eve Davis'],\n"
    "    'email':     ['alice@gmail.com','bob@yahoo.com','carol@gmail.com','dave@company.org','eve@yahoo.com'],\n"
    "    'phone':     ['212-555-1234','555-1234','310-555-9876','212-555-4321','(415)555-0000'],\n"
    "})\n"
    "users['domain'] = users['email'].str.split('@').str[1]\n"
    "users['first_name'] = users['full_name'].str.split().str[0]\n"
    "users['last_name']  = users['full_name'].str.split().str[-1]\n"
    "users['username']   = (users['first_name'].str.lower() + users['last_name'].str[0].str.lower())\n"
    "users['valid_phone'] = users['phone'].str.match(r'^\\d{3}-\\d{3}-\\d{4}$')\n"
    "print(users)\n"
    "print('Users per domain:')\n"
    "print(users['domain'].value_counts())"
))

# Solution 6
cells.append(md("## Solution 6 — DateTime Operations"))
cells.append(code(
    "dates = pd.date_range('2024-01-01', periods=60, freq='D')\n"
    "traffic = pd.DataFrame({'date': dates.strftime('%Y-%m-%d'),'visits': np.random.randint(1000,10000,60),'bounces': np.random.randint(200,5000,60)})\n"
    "traffic['date'] = pd.to_datetime(traffic['date'])\n"
    "traffic['year'] = traffic['date'].dt.year\n"
    "traffic['month'] = traffic['date'].dt.month\n"
    "traffic['day_of_week'] = traffic['date'].dt.dayofweek\n"
    "weekdays = traffic[traffic['day_of_week'] < 5]\n"
    "peak = traffic.loc[traffic['visits'].idxmax(), 'date']\n"
    "print('Peak date:', peak.date())\n"
    "traffic['7d_rolling_avg'] = traffic['visits'].rolling(7).mean().round(0)\n"
    "print(traffic[['date','visits','7d_rolling_avg']].tail(10))"
))

# Solution 7
cells.append(md("## Solution 7 — Pivot Tables"))
cells.append(code(
    "np.random.seed(0)\n"
    "n = 200\n"
    "store_sales = pd.DataFrame({'month':np.random.choice(['Jan','Feb','Mar','Apr'],n),'region':np.random.choice(['North','South','East','West'],n),'product':np.random.choice(['Widget','Gadget','Doohickey'],n),'revenue':np.random.randint(100,5000,n)})\n"
    "pivot = store_sales.pivot_table(index='region', columns='product', values='revenue', aggfunc='sum')\n"
    "print('Pivot:')\n"
    "print(pivot)\n"
    "pivot_m = store_sales.pivot_table(index='region', columns='product', values='revenue', aggfunc='sum', margins=True)\n"
    "pivot_m = pivot_m.fillna(0)\n"
    "print('With totals:')\n"
    "print(pivot_m)\n"
    "top_row = store_sales.loc[store_sales['revenue'].idxmax()]\n"
    "print('Highest single revenue:', top_row.to_dict())\n"
    "long = pivot.reset_index().melt(id_vars='region', var_name='product', value_name='revenue')\n"
    "print('Long format:')\n"
    "print(long.head())"
))

# Solution 8
cells.append(md("## Solution 8 — Apply & Custom Functions"))
cells.append(code(
    "np.random.seed(7)\n"
    "n = 300\n"
    "loans = pd.DataFrame({'applicant_id':range(1,n+1),'income':np.random.randint(25000,150000,n),'debt':np.random.randint(5000,80000,n),'credit_score':np.random.randint(300,850,n)})\n"
    "loans['debt_ratio'] = (loans['debt'] / loans['income']).round(2)\n"
    "loans['risk_score'] = ((loans['credit_score'] - 300) / (850 - 300) * 100).round(1)\n"
    "loans['risk_category'] = pd.cut(loans['risk_score'], bins=[-1,40,70,101], labels=['High','Medium','Low'])\n"
    "loans['approved'] = (loans['debt_ratio'] < 0.4) & (loans['risk_score'] >= 60)\n"
    "approval_rate = loans.groupby('risk_category', observed=True)['approved'].mean().round(3)\n"
    "print('Approval rate per risk category:')\n"
    "print(approval_rate)"
))

# Solution 9
cells.append(md("## Solution 9 — Window Functions"))
cells.append(code(
    "np.random.seed(42)\n"
    "dates = pd.date_range('2024-01-01', periods=120, freq='B')\n"
    "returns = np.random.normal(0.0005, 0.015, 120)\n"
    "prices = 100 * np.cumprod(1 + returns)\n"
    "stock = pd.DataFrame({'close': prices.round(2)}, index=dates)\n"
    "stock['5d_ma'] = stock['close'].rolling(5).mean().round(2)\n"
    "stock['20d_ma'] = stock['close'].rolling(20).mean().round(2)\n"
    "stock['pct_change'] = stock['close'].pct_change().round(4)\n"
    "stock['big_move'] = stock['pct_change'].abs() > 0.03\n"
    "stock['cum_return'] = (stock['close'] / stock['close'].iloc[0]).round(4)\n"
    "rolling_max = stock['close'].cummax()\n"
    "stock['drawdown'] = ((stock['close'] - rolling_max) / rolling_max).round(4)\n"
    "print('Max drawdown:', stock['drawdown'].min())\n"
    "prev_above = stock['5d_ma'] > stock['20d_ma']\n"
    "curr_above = stock['5d_ma'] > stock['20d_ma']\n"
    "stock['signal'] = 'HOLD'\n"
    "cross_above = (~prev_above.shift(1).fillna(False)) & curr_above\n"
    "cross_below = prev_above.shift(1).fillna(False) & (~curr_above)\n"
    "stock.loc[cross_above, 'signal'] = 'BUY'\n"
    "stock.loc[cross_below, 'signal'] = 'SELL'\n"
    "print(stock[['close','5d_ma','20d_ma','signal']].dropna().tail(10))"
))

# Solution 10
cells.append(md("## Solution 10 — E-Commerce Mini Project"))
cells.append(code(
    "from io import StringIO\n"
    "np.random.seed(42)\n"
    "n = 500\n"
    "ecommerce = pd.DataFrame({\n"
    "    'order_id':    range(1001, 1001+n),\n"
    "    'customer_id': np.random.choice([f'C{i:03d}' for i in range(1,81)] + [None], n, p=[1/81]*80 + [1/81]),\n"
    "    'order_date':  pd.date_range('2023-01-01', periods=n, freq='14H').strftime('%Y-%m-%d'),\n"
    "    'category':    np.random.choice(['Electronics','Clothing','Books','Home','Sports'], n),\n"
    "    'quantity':    np.random.randint(1, 6, n),\n"
    "    'unit_price':  np.random.choice([9.99,19.99,49.99,99.99,199.99], n),\n"
    "    'discount':    np.random.choice([0, 0, 0, 0.1, 0.2, None], n),\n"
    "})\n"
    "print('Shape:', ecommerce.shape)\n"
    "ecommerce['order_date'] = pd.to_datetime(ecommerce['order_date'])\n"
    "ecommerce['discount'] = ecommerce['discount'].fillna(0)\n"
    "ecommerce = ecommerce.dropna(subset=['customer_id'])\n"
    "ecommerce['net_revenue'] = (ecommerce['quantity'] * ecommerce['unit_price'] * (1 - ecommerce['discount'])).round(2)\n"
    "monthly = ecommerce.groupby(ecommerce['order_date'].dt.to_period('M'))['net_revenue'].sum()\n"
    "print('Monthly revenue:')\n"
    "print(monthly)\n"
    "top5 = ecommerce.groupby('customer_id')['net_revenue'].sum().nlargest(5)\n"
    "print('Top 5 customers:')\n"
    "print(top5)\n"
    "cat = ecommerce.groupby('category').agg(total_orders=('order_id','count'), avg_order_value=('net_revenue','mean')).round(2)\n"
    "print('Category performance:')\n"
    "print(cat)\n"
    "first_order = ecommerce.groupby('customer_id')['order_date'].min().dt.to_period('M').rename('first_order_month')\n"
    "ecommerce = ecommerce.join(first_order, on='customer_id')\n"
    "order_counts = ecommerce.groupby('customer_id')['order_id'].count()\n"
    "ecommerce['is_repeat'] = ecommerce['customer_id'].map(order_counts) > 1\n"
    "print('Repeat customers:', ecommerce['is_repeat'].sum())\n"
    "summary = cat.reset_index()\n"
    "buf = StringIO()\n"
    "summary.to_csv(buf, index=False)\n"
    "print('CSV preview:')\n"
    "print(buf.getvalue())"
))

# ── Write notebook ────────────────────────────────────────────────────────
nb = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"}
    },
    "cells": cells
}

path = os.path.join(OUT, "pandas_practice.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

nb_cells = len(cells)
size_kb = os.path.getsize(path) / 1024
print(f"Created: {path}")
print(f"  {nb_cells} cells | {size_kb:.1f} KB")
print(f"  10 exercises + 10 solutions")
