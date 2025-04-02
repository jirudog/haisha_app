import streamlit as st
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Google APIのスコープ設定
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Streamlit secrets からサービスアカウント情報を取得
credentials_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, SCOPE)

# スプレッドシートIDとシート名
SPREADSHEET_ID = "18M4Kh_wpv-NUlLdy0cH-3TN0Trxsapluskmpwv_oFMk"
SHEET_NAME = "シート1"

# データ取得関数
def load_driver_data():
    try:
        client = gspread.authorize(credentials)
        worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        df.columns = ["管理番号", "名前", "所属地域"]
        return df
    except Exception as e:
        st.error(f"スプレッドシートの読み込みに失敗しました: {e}")
        return pd.DataFrame()

# --- アプリ構成 ---
st.set_page_config(page_title="配車アプリ", layout="centered")
st.title("🚚 配車アプリ")

# データ取得
df = load_driver_data()
if df.empty:
    st.stop()

# --- リーダー選出 ---
st.markdown("### 👤 本日のリーダー選出")
leader_candidates = ["石井", "梅津", "小平佳代子"]
selected_leader = st.radio("リーダーを1名選んでください", leader_candidates, horizontal=True)

if st.button("✅ リーダーを確定"):
    st.success(f"本日のリーダーは {selected_leader} さんです！")

# --- 出荷従事者選出 ---
st.markdown("### 📦 本日の従事者（各便1名）")
workers = ["石井", "小平", "梅津", "長", "小鮒", "澤田", "中島", "登田"]

col1, col2, col3 = st.columns(3)
with col1:
    worker1 = st.selectbox("1便担当", workers)
with col2:
    worker2 = st.selectbox("2便担当", workers)
with col3:
    worker3 = st.selectbox("3便担当", workers)

if st.button("🚛 従事者を確定"):
    st.success(f"1便：{worker1} さん、2便：{worker2} さん、3便：{worker3} さん")

# --- 病院登録機能 ---
st.markdown("### 🏥 配送先の病院登録")
if "hospital_list" not in st.session_state:
    st.session_state.hospital_list = []

with st.form("hospital_form"):
    hospital_name = st.text_input("病院名（必須）")
    hospital_note = st.text_input("備考（任意）")
    submitted = st.form_submit_button("➕ 登録")
    if submitted and hospital_name:
        st.session_state.hospital_list.append({"病院名": hospital_name, "備考": hospital_note})
        st.success(f"{hospital_name} を登録しました")

if st.session_state.hospital_list:
    st.markdown("#### 📑 登録済みの病院一覧")
    st.table(pd.DataFrame(st.session_state.hospital_list))

# --- ドライバー名簿（参考用） ---
with st.expander("📋 全ドライバー一覧（参考）"):
    st.dataframe(df, use_container_width=True)
