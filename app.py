# 建立一個簡易版「百家樂預測小工具」Streamlit App 程式碼（純邏輯 + 預測建議）
baccarat_predictor_code = '''
import streamlit as st
import random

st.set_page_config(page_title="百家樂預測小工具", layout="centered")
st.title("🎴 百家樂預測小工具")
st.markdown("模擬百家樂遊戲走勢，自動預測下一局趨勢方向。適用於練習判斷、策略模擬用途。")

# 遊戲歷史記錄（使用 session state 保存）
if "history" not in st.session_state:
    st.session_state.history = []

# 預測邏輯（簡易版：統計目前出現最多的連莊方）
def predict_next(history):
    if not history:
        return "請先記錄幾局結果"
    # 分析最近幾局
    recent = history[-6:]
    count = {"閒": 0, "莊": 0}
    for h in recent:
        if h in count:
            count[h] += 1
    if count["閒"] > count["莊"]:
        return "預測：莊家反彈"
    elif count["莊"] > count["閒"]:
        return "預測：閒家反彈"
    else:
        return "預測：持續震盪，觀望為宜"

# 使用者輸入
st.markdown("### ➤ 輸入本局結果")
col1, col2, col3 = st.columns(3)
if col1.button("莊贏"):
    st.session_state.history.append("莊")
if col2.button("閒贏"):
    st.session_state.history.append("閒")
if col3.button("平手"):
    st.session_state.history.append("和")

# 顯示歷史紀錄
if st.session_state.history:
    st.markdown("### 🎲 歷史記錄")
    st.write(" → ".join(st.session_state.history[-20:]))

    st.markdown("### 🤖 預測建議")
    st.success(predict_next(st.session_state.history))

# 重設按鈕
if st.button("🔄 清除紀錄"):
    st.session_state.history = []
'''

# requirements.txt
requirements = "streamlit\n"

# 儲存為部署用檔案
with open("/mnt/data/app.py", "w", encoding="utf-8") as f:
    f.write(baccarat_predictor_code)

with open("/mnt/data/requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements)

# 壓縮成 ZIP
from zipfile import ZipFile
zip_path = "/mnt/data/百家樂預測小工具.zip"
with ZipFile(zip_path, "w") as zipf:
    zipf.write("/mnt/data/app.py", arcname="app.py")
    zipf.write("/mnt/data/requirements.txt", arcname="requirements.txt")

zip_path
