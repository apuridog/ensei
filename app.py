import streamlit as st
from datetime import datetime
import urllib.parse

# --- ページ設定 ---
st.set_page_config(page_title="遠征告知ツール", layout="centered")

st.title("🏀 遠征告知作成ツール")

# --- 1. 会場と住所検索 ---
st.header("1. 会場・住所の設定")
venue_name = st.text_input("会場名（学校名や体育館名）", "江戸川区立小松川第二中学校")

# Googleマップ検索リンクの生成
encoded_venue = urllib.parse.quote(venue_name)
google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_venue}"

st.write("▼ 会場の住所がわからない場合はこちら")
st.link_button("🗺️ Googleマップで住所を検索する", google_maps_url)

address = st.text_input("会場住所", "東京都江戸川区小松川２丁目１０−２")


# --- 2. 日時・スケジュールの設定 ---
st.header("2. 日時・スケジュール")
col1, col2 = st.columns([2, 1])
with col1:
    date = st.date_input("試合日程", datetime.now())
with col2:
    is_holiday = st.checkbox("祝日マーク(・祝)をつける", value=False)

col3, col4 = st.columns(2)
with col3:
    time_shinjuku = st.text_input("①新宿駅南口 集合時間", "6:50")
with col4:
    time_local = st.text_input("②現地集合 集合時間", "7:50")

col5, col6 = st.columns(2)
with col5:
    match_start = st.text_input("試合開始予定", "8:00")
with col6:
    match_end = st.text_input("試合終了予定", "12:30")


# --- 3. カテゴリー・参加費 ---
st.header("3. カテゴリー・参加費")
col7, col8 = st.columns(2)
with col7:
    gender = st.selectbox("性別", ["男子", "女子", "男女"])
with col8:
    age_group = st.selectbox("年代", ["U12", "U15", "U12/15"])

fee_option = st.radio("参加費", ["無し", "有り（金額を手入力）"], horizontal=True)
if fee_option == "有り（金額を手入力）":
    fee = st.text_input("参加費を入力", "1,000円")
else:
    fee = "無し"


# --- 4. 緊急連絡先 ---
st.header("4. 緊急連絡先")

# 連絡先データベース
CONTACTS = {
    "鎌田": "080-4835-1204",
    "髙草": "080-2335-6985",
    "その他（手入力）": ""
}

# 担当者の選択
contact_choice = st.selectbox("担当者を選択", list(CONTACTS.keys()))

col9, col10 = st.columns(2)
with col9:
    contact_name = st.text_input("担当者名", contact_choice if contact_choice != "その他（手入力）" else "")
with col10:
    contact_phone = st.text_input("電話番号", CONTACTS.get(contact_choice, "") if contact_choice != "その他（手入力）" else "")


# --- 告知文の組み立てロジック ---
# 曜日の日本語変換＋祝日対応
weeks = ["月", "火", "水", "木", "金", "土", "日"]
day_of_week = weeks[date.weekday()]
if is_holiday:
    day_of_week += "・祝"

# カテゴリーの結合
category_text = f"{gender}{age_group}"

# テンプレートへの流し込み（ご指定のフォーマットに完全準拠）
result_text = f"""【{date.month}/{date.day}({day_of_week}) {venue_name}】

＜集合時間＞
①新宿駅南口 集合時間 {time_shinjuku}
②現地集合 集合時間 {time_local}
ノートのコメント欄に移動方法をお願いします。

＜カテゴリー＞
{category_text}

＜試合時間（予定）＞
・{match_start}~{match_end}

〈参加費〉
{fee}

＜試合会場＞
・{venue_name}
{address}

＜緊急連絡先＞
・{contact_name}
{contact_phone}
＊当日急な体調不良やトラブルなどありましたらご連絡ください。"""


# --- 5. 画面表示 ---
st.divider()
st.subheader("📝 完成した告知文")
st.code(result_text, language="text")
st.info("右上のアイコンをタップしてコピーし、ノート等に貼り付けてください。")
