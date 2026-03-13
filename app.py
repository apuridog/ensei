import streamlit as st
import re
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="遠征告知ツール", layout="centered")
st.title("🏀 遠征告知作成ツール")

# --- 初期値の設定 ---
if 'target_date' not in st.session_state: st.session_state.target_date = datetime.now()
if 'venue_name' not in st.session_state: st.session_state.venue_name = "江戸川区立小松川第二中学校"
if 'time_shinjuku' not in st.session_state: st.session_state.time_shinjuku = "6:50"
if 'time_local' not in st.session_state: st.session_state.time_local = "7:50"
if 'match_start' not in st.session_state: st.session_state.match_start = "8:00"
if 'match_end' not in st.session_state: st.session_state.match_end = "12:30"

# ==========================================
# 0. コピペで自動抽出機能
# ==========================================
st.header("0. 案内文から自動入力 🪄")
pasted_text = st.text_area("ここに案内文を貼り付け", height=100)

if st.button("✨ テキストから日時や場所を自動入力"):
    if pasted_text:
        date_match = re.search(r'(\d{1,2})\s*[月/]\s*(\d{1,2})', pasted_text)
        if date_match:
            try:
                y_now = datetime.now().year
                st.session_state.target_date = datetime(y_now, int(date_match.group(1)), int(date_match.group(2)))
            except: pass

        shinjuku_match = re.search(r'新宿.*?(\d{1,2}[:：]\d{2})', pasted_text)
        if shinjuku_match: st.session_state.time_shinjuku = shinjuku_match.group(1).replace('：', ':')

        local_match = re.search(r'現地.*?(\d{1,2}[:：]\d{2})', pasted_text)
        if local_match: st.session_state.time_local = local_match.group(1).replace('：', ':')

        match_time = re.search(r'(\d{1,2}[:：]\d{2})\s*[~〜-]\s*(\d{1,2}[:：]\d{2})', pasted_text)
        if match_time:
            st.session_state.match_start = match_time.group(1).replace('：', ':')
            st.session_state.match_end = match_time.group(2).replace('：', ':')

        v_regex = r'([^\s　【】＜＞<>\[\]()（）]+(?:中学校|高校|体育館|スポーツセンター|アリーナ|ドーム))'
        venue_match = re.search(v_regex, pasted_text)
        if venue_match:
            st.session_state.venue_name = venue_match.group(1)

        st.success("読み込み完了！")

# ==========================================
# 1. 会場・住所の設定
# ==========================================
st.header("1. 会場・住所の設定")
venue_name = st.text_input("会場名", key="venue_name")

encoded_venue = urllib.parse.quote(venue_name)
google_maps_search_url = f"https://www.google.com/maps/search/?api=1&query={encoded_venue}"

st.link_button("📍 Googleマップで住所を検索", google_maps_search_url)
address = st.text_input("会場住所", "東京都江戸川区小松川２丁目１０−２")

# ==========================================
# 2. 日時・スケジュールの設定
# ==========================================
st.header("2. 日時・スケジュール")
col1, col2 = st.columns([2, 1])
with col1:
    date = st.date_input("試合日程", key="target_date")
with col2:
    # エラーの原因になりやすい長い文字を短くしました
    is_holiday = st.checkbox("祝日マークをつける", value=False)

col3, col4 = st.columns(2)
with col3:
    time_shinjuku = st.text_input("①新宿駅南口 集合時間", key="time_shinjuku")
with col4:
    time_local = st.text_input("②現地集合 集合時間", key="time_local")

col5, col6 = st.columns(2)
with col5:
    match_start = st.text_input("試合開始予定", key="match_start")
with col6:
    match_end = st.text_input("試合終了予定", key="match_end")

# --- 経路検索 ---
st.subheader("🚃 新宿駅からの乗換案内")
encoded_origin = urllib.parse.quote("新宿駅")
encoded_destination = urllib.parse.quote(address if address else venue_name)

try:
    local_time_obj = datetime.strptime(time_local.replace('：', ':'), "%H:%M").time()
    y, m, d = date.year, f"{date.month:02}", f"{date.day:02}"
    hh = f"{local_time_obj.hour:02}"
    m1, m2 = str(local_time_obj.minute // 10), str(local_time_obj.minute % 10)
    yahoo_url = f"https://transit.yahoo.co.jp/search/result?from={encoded_origin}&to={encoded_destination}&y={y}&m={m}&d={d}&hh={hh}&m1={m1}&m2={m2}&type=4"
except:
    yahoo_url = f"https://transit.yahoo.co.jp/search/result?from={encoded_origin}&to={encoded_destination}&type=4"

st.link_button("🟩 Yahoo!乗換案内（到着時間 指定）", yahoo_url)

# ==========================================
# 3. 年代・参加費
# ==========================================
st.header("3. 年代・参加費")
col7, col8 = st.columns(2)
with col7:
    gender = st.selectbox("性別", ["男子", "女子", "男女"])
with col8:
    age_group = st.selectbox("年代", ["U10", "U12", "U14", "U15", "U12/14", "U12/15"])

fee_option = st.radio("参加費", ["無し", "有り（手入力）"], horizontal=True)
fee = st.text_input("金額", "1,000円") if fee_option == "有り（手入力）" else "無し"

# ==========================================
# 4. 駐車場・注意事項
# ==========================================
st.header("4. 駐車場・注意事項")

parking_options = ["無し（近隣コインパーキング等を利用）", "有り", "未定"]
parking_status = st.radio("駐車場の有無", parking_options, horizontal=True)
parking_notes = st.text_input("駐車場の注意点（任意）")
venue_notes = st.text_area("会場の注意事項（任意）")

# ==========================================
# 5. 緊急連絡先
# ==========================================
st.header("5. 緊急連絡先")
CONTACTS = {"鎌田": "080-4835-1204", "髙草": "080-2335-6985", "その他": ""}
contact_choice = st.selectbox("担当者を選択", list(CONTACTS.keys()))
col9, col10 = st.columns(2)
with col9:
    contact_name = st.text_input("担当者名", contact_choice if contact_choice != "その他" else "")
with col10:
    contact_phone = st.text_input("電話番号", CONTACTS.get(contact_choice, "") if contact_choice != "その他" else "")

# ==========================================
# 告知文の組み立て
# ==========================================
weeks = ["月", "火", "水", "木", "金", "土", "日"]
day_of_week = weeks[date.weekday()]
if is_holiday: day_of_week += "・祝"

parking_text = f"＜駐車場＞\n・{parking_status}"
if parking_notes:
    parking_text += f"\n※{parking_notes}"

venue_notes_text = ""
if venue_notes:
    venue_notes_text = f"\n\n＜会場注意事項＞\n{venue_notes}"

result_text = f"""【{date.month}/{date.day}({day_of_week}) {venue_name}】

＜集合時間＞
①新宿駅南口 集合時間 {time_shinjuku}
②現地集合 集合時間 {time_local}
ノートのコメント欄に移動方法をお願いします。

＜カテゴリー＞
{gender}{age_group}

＜試合時間（予定）＞
・{match_start}~{match_end}

〈参加費〉
{fee}

＜試合会場＞
・{venue_name}
{address}

{parking_text}{venue_notes_text}

＜緊急連絡先〉
・{contact_name}
{contact_phone}
＊当日急な体調不良やトラブルなどありましたらご連絡ください。"""

st.divider()
st.subheader("📝 完成した告知文")
st.code(result_text, language="text")
