import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# ページ設定
st.set_page_config(
    page_title="講義ノート要約＆質問ツール",
    page_icon="📝",
    layout="centered"
)

# --- Gemini API 設定 ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("APIキーが設定されていません。.streamlit/secrets.toml を確認してください。")
    st.stop()

model = genai.GenerativeModel("gemini-3.5-flash")

# --- セッション状態（記憶領域）の初期化 ---
if "summary" not in st.session_state:
    st.session_state.summary = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_content" not in st.session_state:
    st.session_state.input_content = None

# --- UI構築 ---
st.title("📝 講義ノート要約＆質問ツール")
st.write("講義のテキストやファイル（PDF / 画像 / テキスト）をアップロードして要約を作成し、疑問点をAIに質問できます。")

# 入力方法の選択（タブ切り替え）
tab1, tab2 = st.tabs(["📁 ファイルアップロード", "✍️ テキスト直接入力"])

current_input = None

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
            current_input = uploaded_file.read().decode("utf-8")
            st.success("テキストファイルを読み込みました。")
            
        # 画像ファイルの場合
        elif file_type in ["image/png", "image/jpeg"]:
            image = Image.open(uploaded_file)
            st.image(image, caption="アップロードされた画像", use_container_width=True)
            current_input = image
            
        # PDFファイルの場合
        elif file_type == "application/pdf":
            pdf_bytes = uploaded_file.read()
            current_input = {
                "mime_type": "application/pdf",
                "data": pdf_bytes
            }
            st.success(f"PDFファイル「{uploaded_file.name}」を読み込みました。")

# タブ2: テキスト直接入力
with tab2:
    text_input = st.text_area("講義ノートのテキストを貼り付け", height=200)
    if text_input.strip():
        current_input = text_input

# 要約実行ボタン
st.divider()
if st.button("✨ 要約を生成する", type="primary"):
    if current_input is None:
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
                
                if isinstance(current_input, str):
                    response = model.generate_content([prompt, current_input])
                else:
                    response = model.generate_content([prompt, current_input])

                # 生成結果と入力をセッションに保存（チャットで参照するため）
                st.session_state.summary = response.text
                st.session_state.input_content = current_input
                st.session_state.chat_history = []  # 新しい要約作成時はチャット履歴をリセット
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# --- 要約結果 & チャットQ&A表示エリア ---
if st.session_state.summary:
    st.subheader("📊 要約結果")
    st.markdown(st.session_state.summary)
    
    st.divider()
    st.subheader("💬 講義内容についての追加質問")
    st.write("要約や講義資料で分からない点、さらに詳しく知りたい用語などを質問してみましょう。")

    # 過去のチャット履歴を表示
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 質問入力フォーム
    if user_query := st.chat_input("例: 「専門用語の〇〇について、もっと噛み砕いて教えて！」"):
        # ユーザーの質問を表示＆履歴保存
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # AIの回答生成
        with st.chat_message("assistant"):
            with st.spinner("講義資料を参照して回答を作成中..."):
                try:
                    chat_prompt = f"""
                    あなたは大学の丁寧なTA（ティーチングアシスタント）です。
                    以下の「講義資料」と「要約結果」を参考に、学生からの質問に分かりやすく答えてください。

                    【要約結果】
                    {st.session_state.summary}

                    【学生からの質問】
                    {user_query}
                    """
                    
                    content_to_send = [chat_prompt]
                    if st.session_state.input_content is not None:
                        if isinstance(st.session_state.input_content, str):
                            content_to_send.append(f"【元テキスト】\n{st.session_state.input_content}")
                        else:
                            content_to_send.append(st.session_state.input_content)

                    response = model.generate_content(content_to_send)
                    answer = response.text
                    
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"回答生成中にエラーが発生しました: {e}")
