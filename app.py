import streamlit as st
from datetime import datetime, timedelta

# --- ページ設定 ---
st.set_page_config(page_title="遠征告知ツール", layout="centered")

st.title("🏀 遠征告知 & ルート逆算ツール")
st.caption("リスト選択と自由入力、どちらも対応可能です。")

# --- 1. 会場データベース ---
VENUES = {
    "【選択してください】": {"address": "", "travel_min": 0},
    "代々木第二体育館": {"address": "東京都渋谷区神南２丁目１−１", "travel_min": 15},
    "大田区総合体育館": {"address": "東京都大田区東蒲田１丁目１１−１", "travel_min": 40},
    "横浜武道館": {"address": "神奈川県横浜市中区翁町２丁目９−１０", "travel_min": 50},
    "その他（手入力）": {"address": "", "travel_min": 0}
}

# --- 2. 入力エリア ---
st.header("1. 基本設定")
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("試合日程", datetime.now())
with col2:
    event_name = st.text_input("イベント名", "練習試合")

# 会場選択の仕組み
venue_choice = st.selectbox("会場リストから選択", list(VENUES.keys()))
venue_info = VENUES[venue_choice]

# 【重要】「その他」を選んだ時だけ入力欄を表示
if venue_choice == "その他（手入力）" or venue_choice == "【選択してください】":
    final_venue_name = st.text_input("会場名を入力してください", placeholder="例：〇〇中学校")
else:
    # リストから選んだ場合でも、名前を微調整できるようにする
    final_venue_name = st.text_input("会場名（修正も可能です）", value=venue_choice)

# 住所と時間の入力
address = st.text_input("会場住所", value=venue_info["address"], placeholder="例：東京都新宿区...")
travel_time = st.number_input("新宿駅からの移動時間（分）", value=venue_info["travel_min"])

st.header("2. 時間の設定")
col3, col4 = st.columns(2)
with col3:
    local_time = st.time_input("現地集合時間", datetime.strptime("09:00", "%H:%M"))
with col4:
    buffer_min = st.slider("新宿駅での集合余裕（分）", 0, 30, 10)

# --- 3. ロジック計算 ---
dummy_dt = datetime.combine(date, local_time)
shinjuku_dt = dummy_dt - timedelta(minutes=(travel_time + buffer_min))
shinjuku_time_str = shinjuku_dt.strftime("%H:%M")

weeks = ["月", "火", "水", "木", "金", "土", "日"]
day_of_week = weeks[date.weekday()]

# Googleマップ検索URL（住所があれば作成）
maps_url = f"https://www.google.com/maps/dir/新宿駅/{address}" if address else "住所未入力"

# --- 4. 告知文の組み立て ---
result_text = f"""【{date.month}/{date.day}({day_of_week}) {event_name}】

〈集合時間〉
①新宿駅南口 {shinjuku_time_str}
（移動{travel_time}分 ＋ 集合余裕{buffer_min}分 を考慮）

②現地集合時間 {local_time.strftime("%H:%M")}

〈会場〉
・{final_venue_name}
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
st.info("右上のアイコンをタップしてコピーしてください。")
