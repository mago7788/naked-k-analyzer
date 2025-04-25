
import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="百家樂預測強化版", layout="centered")
st.title("🎴 百家樂預測強化版")
st.markdown("支援自動機率預測、龍寶統計與下注策略模擬（馬丁、1326）")

# 初始化
if "history" not in st.session_state:
    st.session_state.history = []
if "strategy" not in st.session_state:
    st.session_state.strategy = "馬丁"
if "base_bet" not in st.session_state:
    st.session_state.base_bet = 10
if "fund" not in st.session_state:
    st.session_state.fund = 1000
if "loss_streak" not in st.session_state:
    st.session_state.loss_streak = 0
if "step_1326" not in st.session_state:
    st.session_state.step_1326 = 0

# 機率預測
def get_probabilities(history):
    total = len(history)
    count = {"莊": 0, "閒": 0, "和": 0}
    for h in history:
        if h in count:
            count[h] += 1
    if total == 0:
        return count
    return {k: round(v / total * 100, 1) for k, v in count.items()}

# 龍寶判斷
def get_long_streak(history):
    if not history:
        return "尚無紀錄"
    last = history[-1]
    count = 1
    for h in reversed(history[:-1]):
        if h == last:
            count += 1
        else:
            break
    return f"{last}家連勝 {count} 次"

# 策略下注金額計算
def get_bet_amount(strategy, base, win_last):
    if strategy == "馬丁":
        return base * (2 ** st.session_state.loss_streak)
    elif strategy == "1326":
        steps = [1, 3, 2, 6]
        return base * steps[st.session_state.step_1326]
    else:
        return base

# 策略模擬更新資金與狀態
def update_strategy(result, bet_on):
    win = result == bet_on
    bet = get_bet_amount(st.session_state.strategy, st.session_state.base_bet, win)

    if win:
        st.session_state.fund += bet
        st.success(f"✔ 贏了 ${bet}！")
        st.session_state.loss_streak = 0
        if st.session_state.strategy == "1326":
            st.session_state.step_1326 = min(3, st.session_state.step_1326 + 1)
    else:
        st.session_state.fund -= bet
        st.error(f"✘ 輸了 ${bet}...")
        st.session_state.loss_streak += 1
        if st.session_state.strategy == "1326":
            st.session_state.step_1326 = 0

# 策略選擇
st.sidebar.markdown("🎯 **策略模擬設定**")
strategy = st.sidebar.selectbox("選擇下注策略", ["馬丁", "1326", "固定金額"])
base_bet = st.sidebar.number_input("基礎注額", value=10, step=5)
st.session_state.strategy = strategy
st.session_state.base_bet = base_bet

# 使用者操作
st.markdown("### ➤ 輸入本局結果")
col1, col2, col3 = st.columns(3)
if col1.button("莊贏"):
    st.session_state.history.append("莊")
    update_strategy("莊", "莊")
if col2.button("閒贏"):
    st.session_state.history.append("閒")
    update_strategy("閒", "莊")
if col3.button("和局"):
    st.session_state.history.append("和")
    update_strategy("和", "莊")

# 顯示統計
if st.session_state.history:
    st.markdown("### 📊 機率預測")
    probs = get_probabilities(st.session_state.history)
    df = pd.DataFrame.from_dict(probs, orient="index", columns=["%"])
    st.bar_chart(df)

    st.markdown("### 🐉 龍寶偵測")
    st.info(get_long_streak(st.session_state.history))

    st.markdown("### 💰 策略模擬結果")
    st.write(f"目前資金：${st.session_state.fund}")
    st.write(f"目前連輸次數：{st.session_state.loss_streak}（馬丁用）")
    st.write(f"1326 步驟：{st.session_state.step_1326+1} / 4")

    st.markdown("### 🎲 歷史記錄")
    st.write(" → ".join(st.session_state.history[-30:]))

if st.button("🔄 清除所有紀錄"):
    st.session_state.history = []
    st.session_state.fund = 1000
    st.session_state.loss_streak = 0
    st.session_state.step_1326 = 0
    st.success("已重置模擬狀態")
