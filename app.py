import streamlit as st
import re
from datetime import datetime
import urllib.parse

# --- ページ設定 ---
st.set_page_config(page_title="遠征告知ツール", layout="centered")

st.title("🏀 遠征告知作成ツール")

# --- 初期値の設定（自動入力機能のため） ---
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
st.caption("LINE等で送られてきた試合の案内文をコピペしてボタンを押すと、下の項目を自動で埋めます！")
pasted_text = st.text_area("ここに案内文を貼り付け", height=100, placeholder="例：3/20 新宿6:50集合 江戸川区立小松川第二中学校 試合8:00~12:30")

if st.button("✨ テキストから日時や場所を自動入力"):
    if pasted_text:
        # 日付の抽出 (例: 3/20 や 3月20日)
        date_match = re.search(r'(\d{1,2})\s*[月/]\s*(\d{1,2})', pasted_text)
        if date_match:
            try:
                year = datetime.now().year
                st.session_state.target_date = datetime(year, int(date_match.group(1)), int(date_match.group(2)))
            except: pass

        # 新宿集合時間の抽出
        shinjuku_match = re.search(r'新宿.*?(\d{1,2}[:：]\d{2})', pasted_text)
        if shinjuku_match: st.session_state.time_shinjuku = shinjuku_match.group(1).replace('：', ':')

        # 現地集合時間の抽出
        local_match = re.search(r'現地.*?(\d{1,2}[:：]\d{2})', pasted_text)
        if local_match: st.session_state.time_local = local_match.group(1).replace('：', ':')

        # 試合時間の抽出 (例: 8:00~12:30)
        match_time = re.search(r'(\d{1,2}[:：]\d{2})\s*[~〜-]\s*(\d{1,2}[:：]\d{2})', pasted_text)
        if match_time:
            st.session_state.match_start = match_time.group(1).replace('：', ':')
            st.session_state.match_end = match_time.group(2).replace('：', ':')

        # 会場名の抽出 (中学校、体育館などの文字を探す)
        venue_match = re.search(r'([^\s　【】＜＞<>\[\]()（）]+(?:中学校|高等学校|高校|体育館|スポーツセンター|アリーナ|武道館|ドーム))', pasted_text)
        if venue_match:
            st.session_state.venue_name = venue_match.group(1)

        st.success("読み込み完了！下の項目に反映しました（※読み取れなかった部分は手入力で補ってください）")


# ==========================================
# 1. 会場・住所の設定
# ==========================================
st.header("1. 会場・住所の設定")
# keyを設定することで、上の自動抽出結果がここに入ります
venue_name = st.text_input("会場名（学校名や体育館名）", key="venue_name")

# Googleマップ検索リンク（スマホ対応の公式URLに変更しました）
encoded_venue = urllib.parse.quote(venue_name)
google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_venue}"

st.write("▼ 会場の住所がわからない場合はこちら")
st.link_button("🗺️ Googleマップで住所を検索する", google_maps_url)

address = st.text_input("会場住所", "東京都江戸川区小松川２丁目１０−２")


# ==========================================
# 2. 日時・スケジュールの設定
# ==========================================
st.header("2. 日時・スケジュール")
col1, col2 = st.columns([2, 1])
with col1:
    date = st.date_input("試合日程", key="target_date")
with col2:
    is_holiday = st.checkbox("祝日マーク(・祝)をつける", value=False)

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


# ==========================================
# 3. カテゴリー・参加費
# ==========================================
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


# ==========================================
# 4. 緊急連絡先
# ==========================================
st.header("4. 緊急連絡先")

CONTACTS = {
    "鎌田": "080-4835-1204",
    "髙草": "080-2335-6985",
    "その他（手入力）": ""
}

contact_choice = st.selectbox("担当者を選択", list(CONTACTS.keys()))

col9, col10 = st.columns(2)
with col9:
    contact_name = st.text_input("担当者名", contact_choice if contact_choice != "その他（手入力）" else "")
with col10:
    contact_phone = st.text_input("電話番号", CONTACTS.get(contact_choice, "") if contact_choice != "その他（手入力）" else "")


# ==========================================
# 告知文の組み立てロジック
# ==========================================
weeks = ["月", "火", "水", "木", "金", "土", "日"]
day_of_week = weeks[date.weekday()]
if is_holiday:
    day_of_week += "・祝"

category_text = f"{gender}{age_group}"

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


# ==========================================
# 5. 画面表示
# ==========================================
st.divider()
st.subheader("📝 完成した告知文")
st.code(result_text, language="text")
st.info("右上のアイコンをタップしてコピーし、ノート等に貼り付けてください。")
