# 📝 講義ノート要約＆復習クイズアプリ

大学の講義ノートや資料をアップロードするだけで、AIが「要約」「復習クイズ」「質問への回答」を行ってくれるWebアプリです。

以下のリンクから、ブラウザ上で実際にアプリをお試しいただけます。
👉 https://note-summarizer-8nzxeuztjnx5mzoppl6mle.streamlit.app/
---

## 主な機能と特徴

1. **マルチモーダル入力対応**
   - テキストの直接入力に加え、PDF・画像（PNG/JPG）・テキストファイル（.txt)のアップロードに対応。
2. **AIによる構造化要約生成**
   - Google Gemini API (`gemini-1.5-flash`) を活用し、「講義概要」「重要キーワード」「箇条書きポイント」の3項目で自動要約。
3. **オンデマンド型 復習クイズ機能（3択問題×3問）**
   - ユーザーが「復習クイズに挑戦する」ボタンを押したタイミングで、講義内容に沿った3択クイズを自動作成。
   - 画面上のラジオボタンで回答を選択し、即座に「自動採点・正解・詳細な解説」を表示。
4. **文脈を保持した Q&A チャット**
   - 資料と要約の文脈（Context）を保持したまま、AI（ティーチングアシスタント）に追加質問が可能。
5. **サイドバー履歴管理**
   - `st.session_state` と `st.rerun()` を用いて、過去に作成した要約や質問ログをサイドバーへ自動保持・即時反映。
6. **テキストダウンロード機能**
   - 生成された要約結果とQ&Aのやり取りを一発で `.txt` ファイルとしてローカルへ保存可能。

## 使用技術

- Language: Python 3.12 
- Framework: Streamlit
- SDK: google-genai (Gemini API / gemini-3.6-flash)
- Deployment: Streamlit Community Cloud
- Version Control: Git / GitHub

---

## 開発で工夫したポイント

- コストとレスポンス速度の最適化:
無駄なAPI呼び出しを防ぐため、Python側で前処理（入力値の最小文字数チェック）を実施。

- ユーザー体験と耐障害性の向上:
API通信時の混雑エラーが発生しても自動で復旧するよう、バックグラウンドでリトライを行う設計を採用。

- セキュリティとエラー防止:
APIキーの秘匿化（Secrets設定）に加え、設定ミスの原因になりやすい全角文字の混入を事前に検知する安全設計を導入。

---

1. リポジトリのクローン
```bash
git clone https://github.com/eik016/note-summarizer.git
cd note-summarizer
```
2. 依存ライブラリのインストール
```bash
pip install -r requirements.txt
```
3. 環境変数の設定

`.streamlit/secrets.toml` ファイルを作成し、ご自身のGemini APIキーを設定します。

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```
4．アプリの起動
```bash
python -m streamlit run app.py
```
