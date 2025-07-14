import os
import fitz
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
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

# 日本語フォント登録（IPAexゴシック）
font_path = "ipaexg.ttf"
pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))

# PDFファイル読み込み
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 要約PDF出力
def save_summary_to_pdf(summary_text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("IPAexGothic", 12)
    width, height = A4
    x, y = 50, height - 50

    for line in summary_text.split("\n"):
        if y < 50:
            c.showPage()
            c.setFont("IPAexGothic", 12)
            y = height - 50
        c.drawString(x, y, line)
        y -= 18
    c.save()

# ディレクトリ設定
input_dir = "授業ノート"
output_dir = "結果"
os.makedirs(output_dir, exist_ok=True)

# PDF処理
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        print(f"\n📄 ファイル: {filename}")

        try:
            content = extract_text_from_pdf(pdf_path)
            if len(content.strip()) == 0:
                print("⚠ テキストが抽出できません。スキップ。")
                continue
        except Exception as e:
            print(f"⚠ 抽出エラー: {e}")
            continue

        prompt = f"以下の大学の授業ノートの内容を要約してください。\n\n{content}"
        try:
            response = model.generate_content(prompt)
            summary = response.text
            print("📝 要約:\n", summary)

            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}_要約.pdf")
            save_summary_to_pdf(summary, output_path)
            print(f"✅ 保存完了: {output_path}")

        except Exception as e:
            print(f"⚠ Gemini API エラー: {e}")
