import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

st.set_page_config(page_title="裸K判斷小工具", layout="centered")

st.title("裸K判斷小工具 🧠")
st.markdown("以下為自動從幣安抓取的 BTC/USDT 15分鐘K線，自動分析趨勢方向與K棒結構。")

# 抓取幣安 K 線資料
def get_binance_klines(symbol="BTCUSDT", interval="15m", limit=5):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    klines = []
    for entry in data:
        ts = datetime.fromtimestamp(int(entry[0]) / 1000).strftime('%Y-%m-%d %H:%M')
        klines.append({
            "時間": ts,
            "開盤": float(entry[1]),
            "最高": float(entry[2]),
            "最低": float(entry[3]),
            "收盤": float(entry[4])
        })
    return pd.DataFrame(klines)

# 裸K判斷邏輯
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

# 趨勢總結
def overall_trend(kbars):
    closes = [row["收盤"] for row in kbars]
    if len(closes) >= 3 and closes[-1] > closes[-2] > closes[-3]:
        return "📈 多方逐漸轉強，偏多操作"
    elif len(closes) >= 3 and closes[-1] < closes[-2] < closes[-3]:
        return "📉 空方主導中，偏空操作"
    else:
        return "⏸ 市場震盪觀望，等待突破"

# 主程式流程
try:
    df = get_binance_klines()
    float_cols = ["開盤", "最高", "最低", "收盤"]
    for col in float_cols:
        df[col] = df[col].astype(float)

    df["K棒解讀"] = df.apply(lambda row: analyze_k(row["開盤"], row["最高"], row["最低"], row["收盤"]), axis=1)
    st.dataframe(df)

    st.subheader("📊 趨勢判斷結果")
    st.success(overall_trend(df.to_dict("records")))

    st.subheader("K棒圖")
    fig, ax = plt.subplots()
    for i, row in df.iterrows():
        color = "green" if row["收盤"] > row["開盤"] else "red"
        ax.plot([i, i], [row["最低"], row["最高"]], color="black")
        ax.plot([i, i], [row["開盤"], row["收盤"]], color=color, linewidth=6)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["時間"].tolist(), rotation=45)
    st.pyplot(fig)

except Exception as e:
    st.error(f"出錯啦：{e}")