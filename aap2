import streamlit as st
from datetime import datetime

# ページの設定
st.set_page_config(page_title="チーム遠征告知作成", layout="centered")

st.title("🏀 遠征告知文作成ツール")
st.caption("情報を入力して、下のボックスからコピーしてください。")

# --- 入力エリア ---
st.header("1. 基本情報")
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("試合日程", datetime.now())
with col2:
    event_name = st.text_input("イベント名", placeholder="例：U-12 練習試合")

st.header("2. 集合・試合時間")
col3, col4, col5 = st.columns(3)
with col3:
    time_shinjuku = st.text_input("①新宿駅集合", "13:00")
with col4:
    time_station = st.text_input("②最寄駅集合", "13:40")
with col5:
    time_local = st.text_input("③現地集合", "14:00")

col6, col7 = st.columns(2)
with col6:
    match_start = st.text_input("試合開始時間", "14:30")
with col7:
    match_end = st.text_input("試合終了予定", "18:00")

st.header("3. 会場・その他")
venue_name = st.text_input("会場名", placeholder="例：〇〇体育館")
address = st.text_input("住所", placeholder="例：東京都〇〇区...")

u12_exists = st.checkbox("U12ゲーム有り", value=True)
fee = st.number_input("参加費（円）", value=1000, step=100)

st.header("4. 緊急連絡先")
col8, col9 = st.columns(2)
with col8:
    contact_name = st.text_input("担当者名", "鎌田")
with col9:
    contact_phone = st.text_input("電話番号", "080-4835-1204")

# --- 文章生成ロジック ---
weeks = ["月", "火", "水", "木", "金", "土", "日"]
day_of_week = weeks[date.weekday()]
u12_msg = "・U12ゲーム有り" if u12_exists else "・U12ゲーム無し"

result_text = f"""【{date.month}/{date.day}({day_of_week}) {event_name}】

〈集合時間〉
①新宿駅南口 {time_shinjuku}
②最寄り駅 {time_station}
③現地集合時間 {time_local}

ノートのコメント欄に移動方法をお願いします。
　
〈試合時間（予定）〉
・{match_start}～{match_end}

〈試合〉
{u12_msg}

〈参加費〉
{fee:,}円

〈試合会場〉
・{venue_name}
  ({address}）

〈緊急連絡先〉
・{contact_name}
{contact_phone}
＊当日急な体調不良やトラブルなどありましたらご連絡ください。"""

# --- 出力エリア ---
st.divider()
st.header("5. 完成した文章")
st.code(result_text, language="text")
st.info("右上のボタンをタップしてコピーし、LINE等に貼り付けてください。")
