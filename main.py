import os
import google.generativeai as genai
from dotenv import load_dotenv  # .envファイルを使う場合はこれも

# .envファイルから環境変数を読み込む（必要な場合）
load_dotenv()  # .envファイルに GOOGLE_API_KEY=xxxxx のように記述

# 環境変数からAPIキーを取得
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY が環境変数に設定されていません")

# APIキーを設定
genai.configure(api_key=api_key)

# モデルの選択
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# 実行例
response = model.generate_content("システムアーキテクチャとは何ですか？")

# 応答を表示
print(response.text)
