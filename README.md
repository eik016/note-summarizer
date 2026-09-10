# 講義ノート要約 & キーワード抽出ツール (note-summarizer)

大学の講義ノートや長文資料を貼り付けるだけで、3行要約、重要キーワード5選、講義の補足ポイントを自動生成する学習支援Webアプリケーション。

Pythonによる事前チェック（ルールベース）とGemini APIによる生成処理（LLM）を組み合わせたハイブリッド構成で開発。

以下のリンクから、ブラウザ上で実際にアプリをお試しいただけます。
👉 https://note-summarizer-8nzxeuztjnx5mzoppl6mle.streamlit.app/
---

## 主な機能と特徴

1. ルールベースとLLMのハイブリッド処理
- リアルタイム分析: 入力されたテキストの総文字数および総行数を即座に計測・表示。
- 事前バリデーション: 50文字未満の入力テキストに対してはAPI呼び出しを行わずエラー警告を表示。不要なAPIリクエストとコストを削減。
- キー安全チェック: 入力されたAPIキーに全角文字や不正文字が含まれていないか事前にASCII判定を実施。

2. Gemini 3.6 Flash による要約・抽出
- 構造化されたプロンプト設計により、一定のフォーマットで再現性の高い要約結果を出力。

3. エラーハンドリングと高可用性
- 自動リトライ処理: サーバー混雑時（503 Unavailable）の自動再試行（最大3回・ウエイト時間付き）を実装。
- Secrets管理: Streamlit CloudのSecrets機能を使用し、APIキーをコード上に直接露出させない安全な環境設定。

---

## 使用技術

- Language: Python 3.12 
- Framework: Streamlit
- SDK: google-genai (Gemini API / gemini-3.6-flash)
- Deployment: Streamlit Community Cloud
- Version Control: Git / GitHub

---

## 開発で工夫したポイント

- コストとレスポンス速度の最適化
無駄なAPI呼び出しを防ぐため、Python側で前処理（入力値の最小文字数チェック）を実施。

- ユーザー体験と耐障害性の向上
API通信時の混雑エラーが発生しても自動で復旧するよう、バックグラウンドでリトライを行う設計を採用。

- セキュリティとエラー防止
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
