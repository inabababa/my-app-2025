import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイル読み込み
load_dotenv()

# APIキー設定
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY が環境変数に設定されていません")
genai.configure(api_key=api_key)

# モデル選択
model = genai.GenerativeModel("models/gemini-2.5-flash")

# PDFファイル読み込み関数
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Markdownファイル保存関数
def save_markdown(content, output_dir, filename, header):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{filename}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {header}\n\n")
        f.write(content.strip())

# ディレクトリ設定
input_dir = "授業ノート"
summary_dir = "要約結果"
exercise_dir = "演習問題"
vocab_dir = "重要単語表"

# PDFファイルを順に処理
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)

        try:
            content = extract_text_from_pdf(pdf_path)
            if len(content.strip()) == 0:
                continue
        except Exception:
            continue

        base_name = os.path.splitext(filename)[0]

        # 要約生成
        try:
            prompt_summary = f"以下は大学の授業ノートの内容です。Markdown形式で簡潔に要約してください。\n\n{content}"
            summary = model.generate_content(prompt_summary).text
            save_markdown(summary, summary_dir, f"{base_name}_要約", "要約")
        except Exception:
            pass

        # 演習問題生成（問題＋解答）
        try:
            prompt_ex = f"以下は大学の授業ノートの内容です。この内容に関する演習問題をMarkdown形式で3問出題し、各問題に模範解答を付けてください。\n\n{content}"
            exercise = model.generate_content(prompt_ex).text
            save_markdown(exercise, exercise_dir, f"{base_name}_演習問題", "演習問題と解答")
        except Exception:
            pass

        # 重要単語帳生成
        try:
            prompt_vocab = f"以下は大学の授業ノートの内容です。この中から重要な専門用語やキーワードを10個抽出し、それぞれ簡潔に説明を加えたMarkdown形式の単語帳を作成してください。\n\n{content}"
            vocab = model.generate_content(prompt_vocab).text
            save_markdown(vocab, vocab_dir, f"{base_name}_重要単語", "重要単語帳")
        except Exception:
            pass
