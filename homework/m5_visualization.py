"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
from itertools import groupby

import matplotlib
matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_bar_category():
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    # TODO: 你的程式碼
    df = _load_data()
    plt.figure(figsize=(8, 4))

    sns.countplot(data=df, x='category', color='steelblue')
    plt.title('Order Count by Category', fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Order Count')
    plt.tight_layout()
    # plt.show()
    fig = plt.gcf()
    return fig


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    df = _load_data()
    plt.figure(figsize=(8, 4))
    sns.histplot(data= df, x= 'amount', kde=True, bins=20)
    plt.xlabel('amount')
    plt.tight_layout()
    # plt.show()
    fig = plt.gcf()
    return fig

def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    # TODO: 你的程式碼
    df = _load_data()
    plt.figure(figsize=(8, 4))

    sns.countplot(data=df, x='category', color='steelblue')
    plt.title('Order Count by Category', fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Order Count')
    plt.tight_layout()
    # plt.show()
    fig = plt.gcf()
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_line_region_trend():
    """
    畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
    - X 軸：月份
    - Y 軸：該月總營收
    - 兩條線，有圖例 (legend)
    回傳 matplotlib Figure 物件
    提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
    """
    # TODO: 你的程式碼
    df = _load_data()
    df = df[df['region'].isin(['North', 'South'])]
    df['month'] = df['order_date'].dt.month
    df = df.groupby(['region', 'month'])['amount'].sum().reset_index()
    # print(df)
    plt.figure(figsize=(8, 4))
    sns.lineplot(data=df, x='month', y='amount', hue='region', marker='o', linewidth=2)
    plt.title('Monthly Revenue: North vs South', fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend(title='Region', loc='upper right')
    plt.tight_layout()
    # plt.show()

    fig = plt.gcf()
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    df = _load_data()
    # print(df.head())
    # df = df.groupby('vip_level')['amount'].reset_index()
    plt.figure(figsize=(8, 4))
    sns.boxplot(x='vip_level', y='amount', data=df)
    plt.title('VIP Level Distribution', fontweight='bold')
    plt.xlabel('VIP Level')
    plt.ylabel('Amount')
    # plt.tight_layout()
    # plt.show()
    fig = plt.gcf()
    return fig

def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    df = _load_data()
    # print(df.head())
    plt.figure(figsize=(8, 4))
    sns.scatterplot(data=df, x='unit_price', y='amount')
    plt.title('Price Amount by Unit', fontweight='bold')
    plt.xlabel('Unit')
    plt.ylabel('Amount')
    plt.tight_layout()
    # plt.show()
    fig = plt.gcf()
    return fig

# tmp = _load_data()
# tmp = green_bar_category()
# tmp = green_hist_amount()
# tmp = green_set_labels()
# tmp = yellow_line_region_trend()
# tmp = yellow_box_vip()
# tmp = yellow_scatter_price_amount()
# print(tmp)

# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_category_dashboard(category="Electronics"):
    """
    針對指定類別，畫 2×2 的 subplot dashboard：
    1. 左上：該類別月營收趨勢 (折線圖)
    2. 右上：該類別各地區營收 (長條圖)
    3. 左下：該類別 Top 5 商品營收 (水平長條圖)
    4. 右下：該類別訂單金額分佈 (直方圖)

    回傳 matplotlib Figure 物件
    提示：fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    """
    # TODO: 你的程式碼
    df = _load_data()
    df['month'] = df['order_date'].dt.month
    df = df[df['category'] == category]
    # print(df.head())
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    df1 = df.groupby('month')['amount'].sum().reset_index()
    sns.lineplot(data=df1, x='month', y='amount', ax=axes[0, 0])
    axes[0, 0].set_title(f'Monthly Revenue: {category}', fontweight='bold')
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('Amount')

    df2 = df.groupby('region')['amount'].sum().reset_index()
    sns.barplot(data=df2, x='region', y='amount', color='steelblue', ax= axes[0, 1])
    axes[0, 1].set_title('Amount by Region', fontweight='bold')
    axes[0, 1].set_xlabel('Region')
    axes[0, 1].set_ylabel('Amount')

    df3 = df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(5).reset_index()
    sns.barplot(data=df3, y='product_name', x='amount', color='steelblue',ax= axes[1, 0])
    axes[1, 0].set_title(f'Top 5 Amount by Product in {category}', fontweight='bold')
    axes[1, 0].set_xlabel('Amount')
    axes[1, 0].set_ylabel('Product')

    # print(df['amount'])
    sns.histplot(data=df['amount'], bins=30, ax=axes[1, 1])
    axes[1, 1].set_title(f'Money Distribution by {category}', fontweight='bold')
    axes[1, 1].set_xlabel('Product')
    axes[1, 1].set_ylabel('Amount')

    fig.tight_layout()
    # plt.show()
    return fig

# red_category_dashboard()