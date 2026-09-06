import streamlit as st
from google import genai
import time

st.set_page_config(page_title="講義ノート要約 & キーワード抽出", page_icon="📝", layout="wide")

st.title("📝 講義ノート要約 & キーワード抽出ツール")
st.write("テキストの自動分析（文字数・行数判定）とGeminiによる要約・用語抽出を組み合わせた学習支援アプリです。")

raw_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Keyを入力", type="password")
api_key = raw_key.strip() if raw_key else ""

if not api_key:
    st.warning("左側のサイドバーにAPIキーを入力するか、Secretsを設定してください。")
    st.stop()

client = genai.Client(api_key=api_key)

user_input = st.text_area("講義ノートや資料のテキストを入力してください:", height=220, placeholder="ここに講義ノートを貼り付けます（50文字以上）")

char_count = len(user_input)
line_count = len(user_input.splitlines()) if user_input else 0

col1, col2, col3 = st.columns(3)
col1.metric("総文字数", f"{char_count} 字")
col2.metric("総行数", f"{line_count} 行")
status_label = "準備完了" if char_count >= 50 else "文字数不足"
col3.metric("入力判定", status_label)

if st.button("ノートを解析する", type="primary"):
    if char_count < 50:
        st.error("入力テキストが短すぎます。50文字以上入力してください。")
    else:
        with st.spinner("AIが講義ノートを整理・要約中..."):
            prompt = f"""
あなたは優秀な大学の学習アシスタントです。
以下の講義ノートを読み、指定されたフォーマットに従って見やすく整理して出力してください。

【出力フォーマット】
### 📌 3行要約
・(箇条書きで1行目)
・(箇条書きで2行目)
・(箇条書きで3行目)

### 🔑 重要キーワード (5選)
1. **[キーワード1]**: 簡潔な説明
2. **[キーワード2]**: 簡潔な説明
3. **[キーワード3]**: 簡潔な説明
4. **[キーワード4]**: 簡潔な説明
5. **[キーワード5]**: 簡潔な説明

### 💡 講義の補足ポイント
(内容を深く理解するためのアドバイスやワンポイント解説)

---
【講義ノート本文】
{user_input}
"""
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                    )
                    st.success("解析が完了しました！")
                    st.markdown("---")
                    st.markdown(response.text)
                    break
                except Exception as e:
                    if "503" in str(e) and attempt < max_retries - 1:
                        time.sleep(2)
                    else:
                        st.error(f"エラーが発生しました: {e}")
                        break
