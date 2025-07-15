import os
from config import setup_api
from pdf_utils import extract_text_from_pdf
from markdown_utils import save_markdown
from generator import generate_summary, generate_exercise, generate_vocab
from pdf_converter import convert_md_to_pdf  # 追加

def process_and_save(model, content, base_name, output_dir, filename_suffix, title):
    md_filename = f"{base_name}_{filename_suffix}.md"
    pdf_filename = f"{base_name}_{filename_suffix}.pdf"

    # Markdown保存
    save_markdown(content, output_dir, base_name + f"_{filename_suffix}", title)
    print(f"{title}のMarkdownファイルを保存しました。")

    # PDF変換パス
    md_path = os.path.join(output_dir, md_filename)
    pdf_path = os.path.join(output_dir, pdf_filename)

    # PDF保存
    convert_md_to_pdf(md_path, pdf_path)

def main():
    print("プログラム開始")
    model = setup_api()

    input_dir = "授業ノート"
    summary_dir = "要約結果"
    exercise_dir = "演習問題"
    vocab_dir = "重要単語表"

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_dir, filename)
        print(f"\n--- {filename} の処理を開始します ---")

        print("PDFからデータを取得中...")
        content = extract_text_from_pdf(pdf_path)
        if not content:
            print("PDFが空または読み込みに失敗しました。スキップします。")
            continue
        print("データを取得しました。")

        base_name = os.path.splitext(filename)[0]

        print("Geminiに要約作成を開始します...")
        summary = generate_summary(model, content)
        print("Geminiから要約作成完了しました。")
        process_and_save(model, summary, base_name, summary_dir, "要約", "要約")

        print("Geminiに演習問題作成を開始します...")
        exercise = generate_exercise(model, content)
        print("Geminiから演習問題作成完了しました。")
        process_and_save(model, exercise, base_name, exercise_dir, "演習問題", "演習問題と解答")

        print("Geminiに重要単語帳作成を開始します...")
        vocab = generate_vocab(model, content)
        print("Geminiから重要単語帳作成完了しました。")
        process_and_save(model, vocab, base_name, vocab_dir, "重要単語", "重要単語帳")

        print(f"--- {filename} の処理が完了しました ---")

    print("\nすべての処理が完了しました。プログラム終了。")

if __name__ == "__main__":
    main()
