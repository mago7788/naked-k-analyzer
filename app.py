import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="裸K判斷小工具", layout="centered")

st.title("裸K判斷小工具 🧠")
st.markdown("輸入最近幾根K線資料（開盤、最高、最低、收盤），系統會分析K棒型態並給出趨勢方向建議。")

num_bars = st.number_input("分析K棒數量", min_value=3, max_value=10, value=3)

k_data = []
for i in range(num_bars):
    st.subheader(f"K{i+1}")
    open_price = st.number_input(f"K{i+1} 開盤", key=f"open_{i}", value=0.0)
    high = st.number_input(f"K{i+1} 最高", key=f"high_{i}", value=0.0)
    low = st.number_input(f"K{i+1} 最低", key=f"low_{i}", value=0.0)
    close = st.number_input(f"K{i+1} 收盤", key=f"close_{i}", value=0.0)
    k_data.append({"開盤": open_price, "最高": high, "最低": low, "收盤": close})

def analyze_k(open_, high, low, close):
    body = abs(close - open_)
    upper_shadow = high - max(open_, close)
    lower_shadow = min(open_, close) - low
    direction = "陽K" if close > open_ else "陰K" if close < open_ else "十字"

    note = f"{direction}，實體:{round(body,2)}，上影:{round(upper_shadow,2)}，下影:{round(lower_shadow,2)}。"

    if lower_shadow > body * 1.5:
        note += " 下影線明顯，多方有支撐。"
    if upper_shadow > body * 1.5:
        note += " 上影線明顯，空方壓力較大。"
    if body < (high - low) * 0.3:
        note += " 短實體或十字，市場猶豫。"
    return note

def overall_trend(kbars):
    closes = [row["收盤"] for row in kbars]
    if len(closes) >= 3 and closes[-1] > closes[-2] > closes[-3]:
        return "📈 多方逐漸轉強，偏多操作"
    elif len(closes) >= 3 and closes[-1] < closes[-2] < closes[-3]:
        return "📉 空方主導中，偏空操作"
    else:
        return "⏸ 市場震盪觀望，等待突破"

if st.button("執行裸K判斷"):
    df = pd.DataFrame(k_data)
    df["K棒解讀"] = df.apply(lambda row: analyze_k(row["開盤"], row["最高"], row["最低"], row["收盤"]), axis=1)
    st.dataframe(df)

    trend = overall_trend(k_data)
    st.subheader("📊 趨勢判斷結果")
    st.success(trend)

    st.subheader("K棒圖")
    fig, ax = plt.subplots()
    for i, row in df.iterrows():
        if row["開盤"] == row["收盤"] == row["最高"] == row["最低"]:
            continue  # 忽略無效K棒
        color = "green" if row["收盤"] > row["開盤"] else "red"
        ax.plot([i, i], [row["最低"], row["最高"]], color="black")
        ax.plot([i, i], [row["開盤"], row["收盤"]], color=color, linewidth=6)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([f"K{i+1}" for i in range(len(df))])
    st.pyplot(fig)
