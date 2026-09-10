import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# ページ設定
st.set_page_config(
    page_title="講義ノート要約ツール",
    page_icon="📝",
    layout="centered"
)

# --- Gemini API 設定 ---
# .streamlit/secrets.toml から API キーを取得
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("APIキーが設定されていません。.streamlit/secrets.toml を確認してください。")
    st.stop()

model = genai.GenerativeModel("gemini-1.5-flash")

# --- UI構築 ---
st.title("📝 講義ノート要約ツール")
st.write("講義のテキストやファイル（PDF / 画像 / テキスト）をアップロードして要約を作成します。")

# 入力方法の選択（タブ切り替え）
tab1, tab2 = st.tabs(["📁 ファイルアップロード", "✍️ テキスト直接入力"])

input_content = None
image_preview = None

# タブ1: ファイルアップロード
with tab1:
    uploaded_file = st.file_uploader(
        "講義資料（PDF、画像、テキストファイル）をアップロードしてください",
        type=["pdf", "png", "jpg", "jpeg", "txt"]
    )
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        
        # テキストファイルの場合
        if file_type == "text/plain":
            input_content = uploaded_file.read().decode("utf-8")
            st.success("テキストファイルを読み込みました。")
            
        # 画像ファイルの場合
        elif file_type in ["image/png", "image/jpeg"]:
            image = Image.open(uploaded_file)
            image_preview = image
            st.image(image, caption="アップロードされた画像", use_container_width=True)
            input_content = image
            
        # PDFファイルの場合
        elif file_type == "application/pdf":
            pdf_bytes = uploaded_file.read()
            input_content = {
                "mime_type": "application/pdf",
                "data": pdf_bytes
            }
            st.success(f"PDFファイル「{uploaded_file.name}」を読み込みました。")

# タブ2: テキスト直接入力
with tab2:
    text_input = st.text_area("講義ノートのテキストを貼り付け", height=200)
    if text_input.strip():
        input_content = text_input

# 要約実行ボタン
st.divider()
if st.button("✨ 要約を生成する", type="primary"):
    if input_content is None:
        st.warning("要約するテキストを入力するか、ファイルをアップロードしてください。")
    else:
        with st.spinner("Gemini APIが要約を生成中..."):
            try:
                prompt = """
                以下の講義資料（またはテキスト）を読み込み、学生の復習用に分かりやすく要約してください。

                【出力フォーマット】
                1. 📌 **講義の概要**（2〜3行で簡潔に）
                2. 🔑 **重要キーワード・専門用語**（3〜5個、簡単な解説つき）
                3. 💡 **要約・ポイントまとめ**（箇条書き）
                """
                
                # 入力データが画像/PDFかテキストかで条件分岐して生成
                if isinstance(input_content, str):
                    response = model.generate_content([prompt, input_content])
                else:
                    response = model.generate_content([prompt, input_content])

                st.subheader("📊 要約結果")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
