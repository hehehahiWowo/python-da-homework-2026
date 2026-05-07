"""
M3 Pandas 進階：merge / groupby / RFM — 課後作業
=================================================
情境：你已經有清理好的訂單資料，現在要合併客戶和商品表，
做出有商業價值的分析。

資料路徑：
  - datasets/ecommerce/orders_clean.csv
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_load_and_merge():
    """
    讀取三張表，合併成一張完整的 DataFrame 並回傳
    - orders_clean.csv LEFT JOIN customers.csv ON customer_id
    - 再 LEFT JOIN products.csv ON product_id
    提示：pd.merge(how='left')
    """
    # TODO: 你的程式碼
    df1 = pd.read_csv('datasets/ecommerce/orders_clean.csv')
    df2 = pd.read_csv('datasets/ecommerce/customers.csv')
    df3 = pd.read_csv('datasets/ecommerce/products.csv')

    df = (
        df1
        .merge(df2, on='customer_id', how='left')
        .merge(df3, on='product_id', how='left')
    )

    # print(df.head())
    # print(df.shape)
    # print(df.columns)
    
    return df


def green_row_count(df):
    """回傳 DataFrame 的列數 (int)"""
    # TODO: 你的程式碼
    # print(len(df))
    return len(df)


def green_column_list(df):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    # TODO: 你的程式碼
    return list(df.columns)


# temp = green_load_and_merge()
# leng = green_row_count(temp)
# leng = green_column_list(temp)
# print(leng)

# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_top_category(df):
    """
    哪個商品類別 (category) 的總營收最高？
    回傳該類別名稱 (str)
    提示：groupby('category')['amount'].sum()
    """
    # TODO: 你的程式碼
    product = df.groupby('category')['amount'].sum().idxmax()
    # print(product)
    return product


def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    提示：df[df['vip_level'] == 'Gold']
    """
    # TODO: 你的程式碼
    order_nums = df[df['vip_level'] == 'Gold']['order_id'].count()
    order_sum = df[df['vip_level'] == 'Gold']['amount'].sum()
    return (order_nums, order_sum)


def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
    提示：groupby('region')['amount'].mean()
    """
    # TODO: 你的程式碼
    avg_money = df.groupby('region')['amount'].mean()
    # print(avg_money)
    # print(type(avg_money))
    return avg_money

# temp = green_load_and_merge()
# tmp = yellow_top_category(temp)
# tmp = yellow_gold_vip_stats(temp)
# tmp = yellow_region_avg_amount(temp)


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_rfm_top5(df):
    """
    RFM 分析：找出最有價值的前 5 位客戶

    計算每位客戶的：
    - R (Recency)：最近一次下單日期
    - F (Frequency)：訂單總數
    - M (Monetary)：消費總金額

    回傳 DataFrame：
    - 欄位：customer_id, customer_name, R, F, M
    - 按 M 由大到小排序
    - 只取前 5 筆

    提示：groupby('customer_id').agg(...)
    """
    # TODO: 你的程式碼
    rfm = df.groupby('customer_id').agg(
        R = ('order_date', 'max'),
        F = ('order_id', 'count'),
        M = ('amount', 'sum')
    )

    cus_name = df[['customer_id', 'customer_name']].drop_duplicates()

    rfm = rfm.merge(
        cus_name,
        on= 'customer_id',
        how='right'
    ).sort_values('M', ascending=False)
    rfm = rfm.head(5).reset_index()[['customer_id', 'customer_name', 'R', 'F', 'M']]
    # print(rfm)
    return rfm

# tmp = red_rfm_top5(temp)