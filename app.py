import streamlit as st
import re
from datetime import datetime
import urllib.parse

# --- ページ設定 ---
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
st.caption("LINE等で送られてきた試合の案内文をコピペしてボタンを押すと、下の項目を自動で埋めます！")
pasted_text = st.text_area("ここに案内文を貼り付け", height=100, placeholder="例：3/20 新宿6:50集合 江戸川区立小松川第二中学校 試合8:00~12:30")

if st.button("✨ テキストから日時や場所を自動入力"):
    if pasted_text:
        date_match = re.search(r'(\d{1,2})\s*[月/]\s*(\d{1,2})', pasted_text)
        if date_match:
            try:
                year = datetime.now().year
                st.session_state.target_date = datetime(year, int(date_match.group(1)), int(date_match.group(2)))
            except: pass

        shinjuku_match = re.search(r'新宿.*?(\d{1,2}[:：]\d{2})', pasted_text)
        if shinjuku_match: st.session_state.time_shinjuku = shinjuku_match.group(1).replace('：', ':')

        local_match = re.search(r'現地.*?(\d{1,2}[:：]\d{2})', pasted_text)
        if local_match: st.session_state.time_local = local_match.group(1).replace('：', ':')

        match_time = re.search(r'(\d{1,2}[:：]\d{2})\s*[~〜-]\s*(\d{1,2}[:：]\d{2})', pasted_text)
        if match_time:
            st.session_state.match_start = match_time.group(1).replace('：', ':')
            st.session_state.match_end = match_time.group(2).replace('：', ':')

        venue_match = re.search(r'([^\s　【】＜＞<>\[\]()（）]+(?:中学校|高等学校|高校|体育館|スポーツセンター|アリーナ|武道館|ドーム))', pasted_text)
        if venue_match:
            st.session_state.venue_name = venue_match.group(1)

        st.success("読み込み完了！下の項目に反映しました")


# ==========================================
# 1. 会場・住所の設定
# ==========================================
st.header("1. 会場・住所の設定")
venue_name = st.text_input("会場名（学校名や体育館名）", key="venue_name")

encoded_venue = urllib.parse.quote(venue_name)
google_maps_search_url = f"https://www.google.com/maps/search/?api=1&query={encoded_venue}"

st.write("▼ 会場の住所がわからない場合はこちら")
st.link_button("📍 Googleマップで住所を検索", google_maps_search_url)

address = st.text_input("会場住所", "東京都江戸川区小松川２丁目１０
