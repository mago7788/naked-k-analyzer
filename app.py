# 重新執行生成 Streamlit app 原型代碼（因執行環境重置）
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="裸K判斷小工具", layout="centered")

st.title("裸K判斷小工具")
st.markdown("輸入最近幾根K線資料（開盤、最高、最低、收盤），系統自動解讀多空趨勢。")

num_bars = st.number_input("輸入要分析的K棒數量", min_value=3, max_value=10, value=3)

k_data = []
for i in range(num_bars):
    st.subheader(f"K{i+1}")
    open_price = st.number_input(f"K{i+1} 開盤價", key=f"open_{i}")
    high = st.number_input(f"K{i+1} 最高價", key=f"high_{i}")
    low = st.number_input(f"K{i+1} 最低價", key=f"low_{i}")
    close = st.number_input(f"K{i+1} 收盤價", key=f"close_{i}")
    k_data.append({"開盤": open_price, "最高": high, "最低": low, "收盤": close})

def analyze_k(open_, high, low, close):
    body = abs(close - open_)
    upper_shadow = high - max(open_, close)
    lower_shadow = min(open_, close) - low
    direction = "陽K" if close > open_ else "陰K"

    note = f"{direction}，實體:{body}，上影:{upper_shadow}，下影:{lower_shadow}。"

    if lower_shadow > body * 1.5:
        note += " 下影線明顯，多方有支撐。"
    if upper_shadow > body * 1.5:
        note += " 上影線明顯，空方壓力較大。"
    if body < (high - low) * 0.3:
        note += " 短實體或十字，市場猶豫。"
    return note

if st.button("執行裸K判斷"):
    df = pd.DataFrame(k_data)
    df["K棒解讀"] = df.apply(lambda row: analyze_k(row["開盤"], row["最高"], row["最低"], row["收盤"]), axis=1)
    st.dataframe(df)

    # K棒圖
    st.subheader("K棒圖")
    fig, ax = plt.subplots()
    for i, row in df.iterrows():
        color = "green" if row["收盤"] > row["開盤"] else "red"
        ax.plot([i, i], [row["最低"], row["最高"]], color="black")
        ax.plot([i, i], [row["開盤"], row["收盤"]], color=color, linewidth=6)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([f"K{i+1}" for i in range(len(df))])
    st.pyplot(fig)
#
file_path

