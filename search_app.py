import streamlit as st
import pandas as pd

# ページのタイトル
st.title('IT導入補助金 交付決定者検索')

# 1. データの読み込み
# Excelファイルが同じフォルダにある前提です
file_name = 'IT_subsidy_data_all.xlsx'

try:
    # データを読み込む（毎回読み込むと遅いのでキャッシュ機能を使います）
    @st.cache_data
    def load_data():
        return pd.read_excel(file_name)

    df = load_data()
    st.success(f"データ読み込み完了: 全 {len(df)} 件")

    # 2. 検索ボックスの表示
    keyword = st.text_input('検索したいキーワード（企業名や法人番号）を入力してください')

    # 3. 検索ロジック
    if keyword:
        # 全ての列を対象に、キーワードが含まれている行を探す
        # (大文字小文字を区別せず、部分一致で探します)
        mask = df.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)
        results = df[mask]

        # 4. 結果の表示
        if not results.empty:
            st.write(f"検索結果: {len(results)} 件 見つかりました")
            st.dataframe(results) # 表を表示
        else:
            st.error("該当なし")

except FileNotFoundError:
    st.error(f"エラー: '{file_name}' が見つかりません。同じフォルダにExcelファイルを置いてください。")