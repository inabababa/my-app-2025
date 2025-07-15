def generate_summary(model, content):
    try:
        prompt = f"以下は大学の授業ノートの内容です。Markdown形式で簡潔に要約してください。\n\n{content}"
        return model.generate_content(prompt).text
    except Exception:
        return ""

def generate_exercise(model, content):
    try:
        prompt = f"以下は大学の授業ノートの内容です。この内容に関する演習問題をMarkdown形式で3問出題し、各問題に模範解答を付けてください。\n\n{content}"
        return model.generate_content(prompt).text
    except Exception:
        return ""

def generate_vocab(model, content):
    try:
        prompt = f"以下は大学の授業ノートの内容です。この中から重要な専門用語やキーワードを10個抽出し、それぞれ簡潔に説明を加えたMarkdown形式の単語帳を作成してください。\n\n{content}"
        return model.generate_content(prompt).text
    except Exception:
        return ""
