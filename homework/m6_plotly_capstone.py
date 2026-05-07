"""
M6 Plotly 互動儀表板 & Capstone — 課後作業
===========================================
情境：從原始資料到互動式儀表板，完成完整的資料分析 pipeline。

資料路徑：
  - datasets/ecommerce/orders_raw.csv（原始髒資料）
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_plotly_bar():
    """
    用 Plotly Express 畫出每個商品類別 (category) 的總營收長條圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.bar()
    """
    # TODO: 你的程式碼
    df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
    # print(df.head())
    df = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(df, x='category', y='amount')
    # fig.show()
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    df = df.groupby('month')['amount'].sum().reset_index()
    fig = px.line(df, x='month', y='amount', markers=True, title='Monthly Revenue')
    fig.update_layout(height=400)
    # fig.show()
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
    df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
    # df = df['vip_level'].value_counts().reset_index()
    df = df.groupby('vip_level')['order_id'].count().reset_index()
    print(df)
    fig = px.pie(df, names='vip_level', values='order_id',
                 title='Number of Orders by VIP Level', hole=0.4)
    fig.update_layout(height=400)
    # fig.show()
    # fig.write_html('first_figure.html', auto_open=True)
    return fig


# green_plotly_bar()
# green_plotly_line()
# green_plotly_pie()

# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：從髒資料到合併完成的 DataFrame
    1. 讀取 orders_raw.csv 並清理（欄位名稱、金額、日期、缺值、去重）
    2. 合併 customers.csv 和 products.csv
    回傳：合併後的 DataFrame
    """
    # TODO: 你的程式碼
    df = pd.read_csv(raw_path)
    df_customers = pd.read_csv(customers_path)
    df_products = pd.read_csv(products_path)

    df.columns = df.columns.str.strip().str.lower()
    df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df = df.dropna(subset=['amount', 'order_date'])
    df = df.drop_duplicates()

    df = (
        df
        .merge(df_customers, how='left', on='customer_id')
        .merge(df_products, how='left', on='product_id')
    )

    df['qty'] = df['qty'].fillna(df['amount']/df['unit_price']).astype(float)
    # print(df.head())
    # print(df.info())
    # print(df_customers.head())
    # print(df_products.head())
    # print(df_customers.info())
    # print(df_products.info())
    return df


def yellow_kpi_summary(df):
    """
    計算 4 個核心 KPI，回傳 dict：
    {
        "total_revenue": float,       # 總營收
        "order_count": int,           # 訂單數
        "active_customers": int,      # 不重複客戶數
        "avg_order_value": float,     # 平均客單價
    }
    """
    # TODO: 你的程式碼
    kpi = {}
    kpi['total_revenue'] = df['amount'].sum().item()
    kpi['order_count'] = df['order_id'].count().item()
    kpi['active_customers'] = df['customer_id'].nunique()
    kpi['avg_order_value'] = df['amount'].mean().item()

    # print(kpi)
    return kpi


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖：
    - X：商品單價 (unit_price)
    - Y：訂單金額 (amount)
    - 顏色：商品類別 (category)
    - hover 顯示：商品名稱 (product_name)
    回傳 plotly Figure 物件
    提示：px.scatter(hover_data=['product_name'])
    """
    # TODO: 你的程式碼
    item = df[['product_name', 'unit_price', 'amount', 'category']]
    # print(item)
    fig = px.scatter(
        item,
        x='unit_price',
        y='amount',
        color='category',
        hover_name='product_name',
        hover_data={
            'unit_price': False,
            'amount': False,
            'category': False
        }
    )

    fig.update_layout(height=400)
    # fig.write_html('first_figure.html', auto_open=True)
    return fig



# temp = yellow_clean_and_merge('../datasets/ecommerce/orders_raw.csv', '../datasets/ecommerce/customers.csv', '../datasets/ecommerce/products.csv')
# tmp = yellow_kpi_summary(temp)
# tmp = yellow_plotly_scatter(temp)

# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    """
    Capstone：完整的互動式儀表板

    流程：
    1. 清理 orders_raw.csv + 合併三張表
    2. 建立 2×2 subplot dashboard（用 plotly make_subplots）：
       - 左上：月營收趨勢 (line)
       - 右上：Top 10 商品營收 (bar)
       - 左下：各地區營收 (bar)
       - 右下：類別營收佔比 (pie/donut)
    3. 設定整體標題

    回傳 plotly Figure 物件
    提示：from plotly.subplots import make_subplots
    """
    # TODO: 你的程式碼
    df = yellow_clean_and_merge('datasets/ecommerce/orders_raw.csv',
                                'datasets/ecommerce/customers.csv',
                                'datasets/ecommerce/products.csv')


    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    df1 = df.groupby('month')['amount'].sum().reset_index()
    fig1 = px.line(df1, x='month', y='amount', markers=True, title='Monthly Revenue Trend')

    df2 = df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(df2, x='product_name', y='amount', title='Top 10 Revenue of Products')

    df3 = df.groupby('region')['amount'].sum().reset_index()
    fig3 = px.bar(df3, x='region', y='amount', title='Revenue of Regions')

    df4 = df.groupby('category')['amount'].sum().reset_index()
    df4['percentage'] = df4['amount'] / df4['amount'].sum() * 100
    fig4 = px.pie(
        df4,
        names='category',
        values='percentage',
        title='Percentage of Revenue by Category'
    )


    fig = make_subplots(rows=2, cols=2,
                        specs=[
                            [{'type': 'xy'}, {'type': 'xy'}],
                            [{'type': 'xy'}, {'type': 'domain'}]
                        ],
                        subplot_titles=(
                            'Monthly Revenue Trend',
                            'Top 10 Revenue of Products',
                            'Revenue of Regions',
                            'Percentage of Revenue by Category'
                        ))
    fig.add_trace(fig1.data[0], row=1, col=1)
    fig.add_trace(fig2.data[0], row=1, col=2)
    fig.add_trace(fig3.data[0], row=2, col=1)
    fig.add_trace(fig4.data[0], row=2, col=2)

    fig.update_layout(title='All Data Dashboard', height=800)
    # fig.write_html('first_figure.html', auto_open=True)
    return fig

# red_dashboard()