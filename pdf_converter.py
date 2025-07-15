# pdf_converter.py
import markdown
from weasyprint import HTML
import os

def convert_md_to_pdf(md_path: str, pdf_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_text = markdown.markdown(md_text)

    HTML(string=html_text).write_pdf(pdf_path)
    print(f"PDFファイルとして保存しました: {pdf_path}")
