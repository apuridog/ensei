import streamlit as st
from datetime import datetime, timedelta

# --- ページ設定 ---
st.set_page_config(page_title="遠征告知ツール", layout="centered")

st.title("🏀 遠征告知 & ルート逆算ツール")
st.caption("会場を選ぶと、新宿駅の出発時間を自動で計算します。")

# --- 1. 会場データベース ---
# ここに新しい会場を追加できます
VENUES = {
    "【会場を選択してください】": {"address": "", "travel_min": 0},
    "代々木第二体育館": {
        "address": "東京都渋谷区神南２丁目１−１",
        "travel_min": 15
    },
    "大田区総合体育館": {
        "address": "東京都大田区東蒲田１丁目１１−１",
        "travel_min": 40
    },
    "横浜武道館": {
        "address": "神奈川県横浜市中区翁町２丁目９−１０",
        "travel_min": 50
    },
    "その他（手入力）": {"address": "", "travel_min": 0}
}

# --- 2. 入力エリア ---
st.header("1. 基本設定")
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("試合日程", datetime.now())
with col2:
    event_name = st.text_input("イベント名", "練習試合")

# 会場選択
venue_choice = st.selectbox("試合会場", list(VENUES.keys()))
venue_info = VENUES[venue_choice]

# 住所と移動時間の取得（自動入力されるが手修正も可能）
address = st.text_input("会場住所", value=venue_info["address"])
travel_time = st.number_input("新宿駅からの移動時間（分）", value=venue_info["travel_min"])

st.header("2. 時間の設定")
col3, col4 = st.columns(2)
with col3:
    local_time = st.time_input("現地集合時間", datetime.strptime("09:00", "%H:%M"))
with col4:
    buffer_min = st.slider("新宿駅での集合余裕（分）", 0, 30, 10)

# --- 3. ロジック計算（逆算） ---
# 現地集合時間 - (移動時間 + 余裕) = 新宿出発時間
dummy_dt = datetime.combine(date, local_time)
shinjuku_dt = dummy_dt - timedelta(minutes=(travel_time + buffer_min))
shinjuku_time_str = shinjuku_dt.strftime("%H:%M")

# 曜日の日本語変換
weeks = ["月", "火", "水", "木", "金", "土", "日"]
day_of_week = weeks[date.weekday()]

# Googleマップ検索URL
maps_url = f"https://www.google.com/maps/dir/新宿駅/{address}/"

# --- 4. 告知文の組み立て ---
result_text = f"""【{date.month}/{date.day}({day_of_week}) {event_name}】

〈集合時間〉
①新宿駅南口 {shinjuku_time_str}
（移動{travel_time}分 ＋ 集合余裕{buffer_min}分 を考慮）

②現地集合時間 {local_time.strftime("%H:%M")}

〈会場〉
・{venue_choice}
 ({address})

〈ルート確認（Googleマップ）〉
{maps_url}

＊当日急なトラブルなどありましたらご連絡ください。"""

# --- 5. 画面表示 ---
st.divider()
st.subheader("💡 逆算されたスケジュール")
st.success(f"新宿駅に **{shinjuku_time_str}** に集合すれば間に合います。")

st.divider()
st.subheader("📝 コピー用テキスト")
st.code(result_text, language="text")
st.info("右上のアイコンをタップしてコピーし、LINE等に貼り付けてください。")
