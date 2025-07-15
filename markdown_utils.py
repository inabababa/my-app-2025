import os

def save_markdown(content, output_dir, filename, header):
    if not content:
        return
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{filename}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {header}\n\n")
        f.write(content.strip())
