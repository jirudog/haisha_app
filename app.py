import streamlit as st
import gspread
import pandas as pd
import json
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

# アプリUI
st.title("🚚 配車アプリ - ドライバー選定")

df = load_driver_data()
if df.empty:
    st.stop()

st.subheader("全ドライバー一覧")
st.dataframe(df)

st.subheader("📋 本日のリーダー選出")
candidates = df["名前"].tolist()
selected = st.radio("リーダーを1名選んでください", candidates)

if st.button("リーダーを確定"):
    st.success(f"✅ 本日の担当者は {selected} さんです！")
