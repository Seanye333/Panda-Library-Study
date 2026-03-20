import json, uuid

NB_PATH = r"c:\Users\seany\Documents\All Codes\Python Panda Library Study\pandas_study_guide.ipynb"

def md(src, cid):
    return {"cell_type":"markdown","id":cid,"metadata":{},"source":src}

def code(src, cid):
    return {"cell_type":"code","execution_count":None,"id":cid,"metadata":{},"outputs":[],"source":src}

new_cells = [

# ── 21. Duplicate Handling ────────────────────────────────────────────────────
code("""\
df_dup = pd.DataFrame({
    'Name':   ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob', 'Alice'],
    'City':   ['NYC',   'LA',  'NYC',   'Chicago',  'LA',  'NYC'],
    'Salary': [70000, 85000, 70000, 90000, 85000, 75000]
})
print("Original:")
print(df_dup)

print("\\nduplication mask (all cols):")
print(df_dup.duplicated())

print("\\nduplication mask (Name only):")
print(df_dup.duplicated(subset=['Name']))\
""", "cell-90"),

code("""\
# --- drop_duplicates ---
print("Drop all full duplicates (keep first):")
print(df_dup.drop_duplicates())

print("\\nDrop by Name, keep first occurrence:")
print(df_dup.drop_duplicates(subset=['Name'], keep='first'))

print("\\nDrop by Name, keep last:")
print(df_dup.drop_duplicates(subset=['Name'], keep='last'))

print("\\nDrop ALL duplicated names (keep none):")
print(df_dup.drop_duplicates(subset=['Name'], keep=False))\
""", "cell-91"),

# ── 22. Binning ───────────────────────────────────────────────────────────────
md("---\n## 22. Binning with cut() and qcut() <a id='22'></a>", "cell-92"),

code("""\
import pandas as pd, numpy as np

data = pd.Series([22, 25, 29, 31, 35, 40, 45, 52, 60, 70])

# --- pd.cut: equal-width bins ---
print("cut (3 equal-width bins):")
print(pd.cut(data, bins=3))

print("\\ncut with custom edges and labels:")
bins   = [0, 25, 40, 100]
labels = ['Young', 'Middle', 'Senior']
print(pd.cut(data, bins=bins, labels=labels))\
""", "cell-93"),

code("""\
# --- pd.qcut: equal-frequency (quantile) bins ---
print("qcut (3 quantile bins):")
print(pd.qcut(data, q=3))

print("\\nqcut with labels:")
print(pd.qcut(data, q=3, labels=['Low', 'Med', 'High']))

# Attach bin to a DataFrame
salaries = pd.Series([65000, 70000, 72000, 85000, 90000, 95000])
df_bin = pd.DataFrame({'Salary': salaries})
df_bin['Band']   = pd.cut(salaries, bins=3, labels=['Low','Mid','High'])
df_bin['Quartile'] = pd.qcut(salaries, q=4, labels=['Q1','Q2','Q3','Q4'])
print(df_bin)\
""", "cell-94"),

# ── 23. assign / pipe / chaining ─────────────────────────────────────────────
md("---\n## 23. assign(), pipe() & Method Chaining <a id='23'></a>", "cell-95"),

code("""\
df_base = pd.DataFrame({
    'Name':   ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Age':    [25, 30, 35, 28, 22],
    'Salary': [70000, 85000, 90000, 72000, 65000],
    'Score':  [88.5, 92.0, 78.3, 95.1, 85.6]
})

# --- assign: add/overwrite columns without mutating the original ---
result = df_base.assign(
    Tax      = lambda x: x['Salary'] * 0.2,
    NetPay   = lambda x: x['Salary'] - x['Salary'] * 0.2,
    Grade    = lambda x: pd.cut(x['Score'], bins=[0,75,85,100],
                                 labels=['C','B','A'])
)
print(result)\
""", "cell-96"),

code("""\
# --- pipe: pass DataFrame into a custom function ---
def normalize_salary(df, col='Salary'):
    df = df.copy()
    df[col + '_norm'] = (df[col] - df[col].mean()) / df[col].std()
    return df

def flag_high_score(df, threshold=88):
    df = df.copy()
    df['TopPerformer'] = df['Score'] > threshold
    return df

# Method chaining using pipe
result = (
    df_base
    .query('Age >= 25')
    .assign(SalaryK=lambda x: (x['Salary'] / 1000).round(1))
    .pipe(normalize_salary)
    .pipe(flag_high_score, threshold=88)
    .sort_values('Salary', ascending=False)
    .reset_index(drop=True)
)
print(result)\
""", "cell-97"),

# ── 24. eval ─────────────────────────────────────────────────────────────────
md("---\n## 24. eval() & Advanced query() <a id='24'></a>", "cell-98"),

code("""\
df_ev = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': [100, 200, 300, 400, 500]
})

# --- df.eval: evaluate a string expression column-wise ---
# Returns the result as a Series
print("A + B * 2:")
print(df_ev.eval('A + B * 2'))

# inplace=True adds the column to the DataFrame
df_ev.eval('D = A + B + C', inplace=True)
df_ev.eval('E = (A * B) / C', inplace=True)
print(df_ev)

# Boolean expression → filter mask
mask = df_ev.eval('A > 2 and B < 50')
print("\\nFilter A>2 and B<50:")
print(df_ev[mask])\
""", "cell-99"),

code("""\
# --- Local variables in eval/query with @ ---
threshold = 30
print("B values > threshold using @:")
print(df_ev.query('B > @threshold'))

# Math functions in eval
df_ev['logC'] = df_ev.eval('log(C)', local_dict={'log': np.log})
print("\\nWith log(C):")
print(df_ev)\
""", "cell-100"),

# ── 25. MultiIndex ────────────────────────────────────────────────────────────
md("---\n## 25. MultiIndex (Hierarchical Indexing) <a id='25'></a>", "cell-101"),

code("""\
# --- Create a MultiIndex Series ---
arrays = [
    ['East', 'East', 'East', 'West', 'West', 'West'],
    ['Q1',   'Q2',   'Q3',   'Q1',   'Q2',   'Q3']
]
idx = pd.MultiIndex.from_arrays(arrays, names=['Region', 'Quarter'])
revenue = pd.Series([120, 150, 130, 200, 220, 180], index=idx, name='Revenue')
print("MultiIndex Series:")
print(revenue)

# Select a level
print("\\nRevenue for East region:")
print(revenue['East'])

print("\\nRevenue for Q1 (all regions):")
print(revenue.xs('Q1', level='Quarter'))\
""", "cell-102"),

code("""\
# --- Create a MultiIndex DataFrame ---
df_mi = pd.DataFrame({
    'Revenue': [120, 150, 130, 200, 220, 180],
    'Cost':    [ 80,  90,  85, 140, 160, 130],
    'Units':   [ 10,  12,  11,  18,  20,  16]
}, index=idx)
print(df_mi)

print("\\nProfit column (Revenue - Cost):")
df_mi['Profit'] = df_mi['Revenue'] - df_mi['Cost']

# loc with tuple for multi-level
print("\\nEast, Q2:")
print(df_mi.loc[('East', 'Q2')])

# Unstack inner level → wide format
print("\\nUnstacked (Quarter as columns):")
print(df_mi['Revenue'].unstack(level='Quarter'))\
""", "cell-103"),

code("""\
# --- Create MultiIndex with from_product ---
regions  = ['East', 'West']
products = ['A', 'B', 'C']
mi = pd.MultiIndex.from_product([regions, products], names=['Region','Product'])
df_prod = pd.DataFrame({'Sales': np.random.randint(100, 500, 6)}, index=mi)
print(df_prod)

# Group-level operations on MultiIndex
print("\\nTotal sales per Region (sum level):")
print(df_prod['Sales'].groupby(level='Region').sum())

print("\\nSwap levels:")
print(df_prod.swaplevel().sort_index())\
""", "cell-104"),

# ── 26. Categorical ───────────────────────────────────────────────────────────
md("---\n## 26. Categorical Data <a id='26'></a>", "cell-105"),

code("""\
# --- Creating Categorical data ---
sizes = pd.Categorical(['M','L','S','XL','M','S'],
                       categories=['S','M','L','XL'],
                       ordered=True)
print("Categorical:", sizes)
print("Categories:", sizes.categories.tolist())
print("Is ordered:", sizes.ordered)
print("Codes (integer encoding):", sizes.codes.tolist())  # memory-efficient

# Comparison works because ordered=True
print("\\nWhere size > M:", (sizes > 'M').tolist())\
""", "cell-106"),

code("""\
# --- Categorical in a DataFrame ---
df_cat = pd.DataFrame({
    'Product': ['Widget','Gadget','Widget','Donut','Gadget','Widget'],
    'Rating':  ['Good','Bad','Excellent','Good','Excellent','Bad'],
    'Size':    ['M','S','L','XL','M','S']
})

# Convert to Categorical
df_cat['Rating'] = pd.Categorical(df_cat['Rating'],
                                  categories=['Bad','Good','Excellent'],
                                  ordered=True)
df_cat['Size'] = pd.Categorical(df_cat['Size'],
                                categories=['S','M','L','XL'],
                                ordered=True)

print(df_cat.dtypes)
print()

# Sorting respects category order
print("Sorted by Rating (category order):")
print(df_cat.sort_values('Rating'))

# groupby with category includes empty groups
df_cat['Count'] = 1
print("\\nCounts per Rating level (including empty):")
print(df_cat.groupby('Rating', observed=False)['Count'].sum())\
""", "cell-107"),

# ── 27. Window Functions ──────────────────────────────────────────────────────
md("---\n## 27. Window Functions (expanding, ewm) <a id='27'></a>", "cell-108"),

code("""\
prices = pd.Series([10, 12, 11, 14, 13, 16, 15, 18, 17, 20],
                   name='Price')

# --- expanding: growing window from start ---
print("Expanding mean (cumulative average):")
print(prices.expanding().mean().round(2))

print("\\nExpanding min / max:")
exp = pd.DataFrame({
    'Price':    prices,
    'exp_mean': prices.expanding().mean().round(2),
    'exp_min':  prices.expanding().min(),
    'exp_max':  prices.expanding().max(),
})
print(exp)\
""", "cell-109"),

code("""\
# --- ewm: Exponentially Weighted Moving Average ---
# span=N: weight decays like a rolling window of size N
# alpha: smoothing factor (0 < alpha <= 1); higher = more weight on recent

print("EWM with span=3:")
print(prices.ewm(span=3).mean().round(3))

print("\\nEWM with alpha=0.3 (explicit smoothing factor):")
print(prices.ewm(alpha=0.3).mean().round(3))

# Compare rolling vs EWM
compare = pd.DataFrame({
    'Price':      prices,
    'Roll3':      prices.rolling(3).mean().round(2),
    'EWM_span3':  prices.ewm(span=3).mean().round(2),
})
print("\\nRolling 3 vs EWM span=3:")
print(compare)\
""", "cell-110"),

# ── 28. Styling ───────────────────────────────────────────────────────────────
md("---\n## 28. DataFrame Styling <a id='28'></a>\n> Styling renders in Jupyter. In plain Python scripts use `.to_html()` to export.", "cell-111"),

code("""\
df_style = pd.DataFrame({
    'Name':   ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Sales':  [120000, 95000, 140000, 88000, 130000],
    'Target': [100000, 100000, 100000, 100000, 100000],
    'Score':  [88.5, 72.0, 95.1, 65.3, 91.2]
})

# --- Basic formatting ---
styled = (df_style.style
    .format({'Sales':  '${:,.0f}',
             'Target': '${:,.0f}',
             'Score':  '{:.1f}%'})
    .set_caption('Sales Performance Report')
)
styled\
""", "cell-112"),

code("""\
# --- Highlight max/min, gradients, bars ---
(df_style.style
    .format({'Sales': '${:,.0f}', 'Score': '{:.1f}'})
    .highlight_max(subset=['Sales', 'Score'], color='#90EE90')
    .highlight_min(subset=['Sales', 'Score'], color='#FFB6C1')
    .background_gradient(subset=['Score'], cmap='RdYlGn')
    .bar(subset=['Sales'], color='#add8e6')
    .set_properties(**{'font-size': '12px'})
)\
""", "cell-113"),

# ── 29. Memory Optimization ───────────────────────────────────────────────────
md("---\n## 29. Memory Optimization <a id='29'></a>", "cell-114"),

code("""\
# Create a large-ish DataFrame to demonstrate memory
np.random.seed(0)
n = 100_000

df_mem = pd.DataFrame({
    'id':       np.random.randint(0, 10000, n),
    'category': np.random.choice(['A','B','C','D','E'], n),
    'value':    np.random.uniform(0, 1000, n),
    'flag':     np.random.randint(0, 2, n),
    'big_int':  np.random.randint(0, 100, n).astype('int64'),
})

def mem_report(df):
    mb = df.memory_usage(deep=True).sum() / 1e6
    print(f"Total memory: {mb:.2f} MB")
    print(df.dtypes)

print("=== Before optimization ===")
mem_report(df_mem)\
""", "cell-115"),

code("""\
df_opt = df_mem.copy()

# Downcast numeric types
df_opt['id']       = pd.to_numeric(df_opt['id'], downcast='unsigned')   # int64→uint16
df_opt['flag']     = df_opt['flag'].astype('int8')
df_opt['big_int']  = df_opt['big_int'].astype('int8')
df_opt['value']    = df_opt['value'].astype('float32')

# Categorical for low-cardinality strings
df_opt['category'] = df_opt['category'].astype('category')

print("=== After optimization ===")
mem_report(df_opt)

before = df_mem.memory_usage(deep=True).sum()
after  = df_opt.memory_usage(deep=True).sum()
print(f"\\nSavings: {(1 - after/before)*100:.1f}%")\
""", "cell-116"),

# ── 30. Sampling ─────────────────────────────────────────────────────────────
md("---\n## 30. Sampling & Random Operations <a id='30'></a>", "cell-117"),

code("""\
df_s = pd.DataFrame({
    'Name':   ['Alice','Bob','Charlie','Diana','Eve','Frank','Grace','Henry'],
    'Dept':   ['Eng','Eng','Mkt','Mkt','HR','Eng','HR','Mkt'],
    'Salary': [90000,85000,70000,72000,65000,95000,68000,75000]
})

# --- Simple random sample ---
print("3 random rows:")
print(df_s.sample(n=3, random_state=42))

print("\\n50% sample:")
print(df_s.sample(frac=0.5, random_state=42))\
""", "cell-118"),

code("""\
# --- Weighted sampling (higher salary = more likely to be picked) ---
print("Weighted sample by Salary:")
print(df_s.sample(n=4, weights='Salary', random_state=42))

# --- Stratified sample: same proportion per group ---
def stratified_sample(df, group_col, frac=0.5, random_state=42):
    return df.groupby(group_col, group_keys=False).apply(
        lambda x: x.sample(frac=frac, random_state=random_state)
    )

print("\\nStratified sample (50% per Dept):")
print(stratified_sample(df_s, 'Dept'))

# --- Shuffle the DataFrame ---
print("\\nShuffled:")
print(df_s.sample(frac=1, random_state=42).reset_index(drop=True))\
""", "cell-119"),

# ── 31. shift & diff ─────────────────────────────────────────────────────────
md("---\n## 31. shift() & diff() for Time Series <a id='31'></a>", "cell-120"),

code("""\
stock = pd.DataFrame({
    'Date':  pd.date_range('2024-01-01', periods=8, freq='B'),
    'Close': [150.0, 152.5, 149.0, 155.0, 157.3, 153.8, 160.0, 162.1]
}).set_index('Date')

# --- shift: lag / lead ---
stock['Prev_Close']  = stock['Close'].shift(1)   # lag 1 day
stock['Next_Close']  = stock['Close'].shift(-1)  # lead 1 day
print("Shift:")
print(stock)\
""", "cell-121"),

code("""\
# --- diff: simple difference ---
stock['Change']    = stock['Close'].diff(1)        # day-over-day change
stock['2day_diff'] = stock['Close'].diff(2)        # 2-period difference

# Percent change
stock['Pct_Change'] = stock['Close'].pct_change().mul(100).round(2)

print("Differences & % change:")
print(stock[['Close','Change','Pct_Change']])

# Detect up/down days
stock['Direction'] = np.where(stock['Change'] > 0, 'UP',
                     np.where(stock['Change'] < 0, 'DOWN', 'FLAT'))
print("\\nDirections:")
print(stock[['Close','Change','Direction']])\
""", "cell-122"),

# ── 32. explode ───────────────────────────────────────────────────────────────
md("---\n## 32. explode() for List Columns <a id='32'></a>", "cell-123"),

code("""\
# --- Basic explode ---
df_exp = pd.DataFrame({
    'OrderID': [1, 2, 3],
    'Items':   [['Apple', 'Banana'], ['Cherry'], ['Apple', 'Cherry', 'Donut']],
    'Customer':['Alice', 'Bob', 'Charlie']
})
print("Before explode:")
print(df_exp)

print("\\nAfter explode:")
exploded = df_exp.explode('Items').reset_index(drop=True)
print(exploded)\
""", "cell-124"),

code("""\
# --- Real-world use: split string → explode ---
df_tags = pd.DataFrame({
    'Article': ['Intro to Pandas', 'Data Cleaning', 'ML with Python'],
    'Tags':    ['pandas,data,python', 'data,cleaning,null', 'ml,python,sklearn']
})

df_tags['TagList'] = df_tags['Tags'].str.split(',')
df_exploded = df_tags.explode('TagList').drop(columns='Tags')
print(df_exploded)

# Count tag frequency
print("\\nTag frequency:")
print(df_exploded['TagList'].value_counts())\
""", "cell-125"),

# ── Final cheatsheet update ───────────────────────────────────────────────────
md("""\
---
## Extended Quick Reference (Topics 21–32)

| Task | Code |
|------|------|
| Find duplicates | `df.duplicated(subset=['col'])` |
| Remove duplicates | `df.drop_duplicates(subset=['col'], keep='first')` |
| Bin into ranges | `pd.cut(s, bins=[0,25,50,100], labels=['L','M','H'])` |
| Equal-freq bins | `pd.qcut(s, q=4, labels=['Q1','Q2','Q3','Q4'])` |
| Add computed cols | `df.assign(Tax=lambda x: x.Salary*0.2)` |
| Chain functions | `df.pipe(my_func).pipe(other_func)` |
| Fast expressions | `df.eval('C = A + B', inplace=True)` |
| MultiIndex select | `df.loc[('East','Q1')]` or `df.xs('Q1', level='Quarter')` |
| Ordered category | `pd.Categorical(s, categories=[...], ordered=True)` |
| Cumulative avg | `s.expanding().mean()` |
| Exponential MA | `s.ewm(span=3).mean()` |
| Style table | `df.style.highlight_max().background_gradient()` |
| Reduce memory | `df['col'].astype('int8')` / `.astype('category')` |
| Random sample | `df.sample(n=5, random_state=42)` |
| Stratified sample | `df.groupby('col').apply(lambda x: x.sample(frac=0.5))` |
| Lag / lead | `s.shift(1)` / `s.shift(-1)` |
| Day-over-day diff | `s.diff(1)` |
| Explode list col | `df.explode('list_col').reset_index(drop=True)` |
""", "cell-126"),
]

with open(NB_PATH, encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'].extend(new_cells)

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Done. Total cells: {len(nb['cells'])}")
