# streamlit_app.py
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime

# # url = "https://docs.google.com/spreadsheets/d/1Gc3Wi1vpTP4g5rnWuaRJDZWycZHvKO7F2xCv1ZGo0oU/edit?usp=sharing"
# # url = "https://docs.google.com/spreadsheets/d/10e1JfvNTklFXhhYsnNMiAUSmKoMSrDI9H5B4zmuAyN4/edit?usp=sharing"
url = "https://docs.google.com/spreadsheets/d/1QQFT8qQRUVaTVJ8QhVBtOe5SXEmt158MM_RHD0-NOpg/edit?usp=sharing"


# ページ定義
def page1(details):
    
    # sheet = conn.read(spreadsheet=url, worksheet="Sheet1")  # シート名を指定して読み込み
    
    notice = details.iloc[1, 0]  # 2行目の1列目をお知らせとして取得
    st.write(f"お知らせ: {notice}")
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url, usecols=[0, 1], ttl=5)  # 1列目と2列目を読み込み
    st.dataframe(data)

    def refresh():
        st.cache_data.clear()  # キャッシュされたデータを削除

    st.button("更新", on_click=refresh)
    # st.header("📅 今日のページ (page1)")
    # st.write("指定された日付が本日と一致しました！")

def page2(details):
    st.header("📅 今日は子ども食堂はお休みです。")
    st.write("次回の開催日は{}です。お楽しみに!!".format(details.iloc[2, 0]))

# メイン処理
def main():
    conn = st.connection("gsheets", type=GSheetsConnection)
    details = conn.read(spreadsheet=url, usecols=[3], ttl=5)  # A列とB列を読み込み
    title = details.iloc[0, 0]  # 1行目の1列目をタイトルとして取得
    st.title(title)

    date_text = details.iloc[2, 0]
    # st.write(f"日付: {date_text}")

    dt = datetime.datetime.strptime(date_text, "%Y/%m/%d").date()
    today = datetime.date.today()
    if dt == today:
            # 今日なら page1へ
        st.query_params.clear()
        st.query_params.update({"page": "page1"})
    else:
            # 違う日付なら page2へ
        st.query_params.clear()
        st.query_params.update({"page": "page2"})


    page = st.query_params.get("page", ["page1"])  # デフォルトは page1
    
    if page == "page1":
        page1(details)
    else:
        page2(details)

if __name__ == "__main__":
    main()
