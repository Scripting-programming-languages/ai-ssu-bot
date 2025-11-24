import json
import re
from pathlib import Path


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text) 
    text = re.sub(r"http\S+", "", text) 
    text = re.sub(r"(наверх|рисунок|фото:.*|изображение:.*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[\*\#•«»\"“”]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, max_len: int = 500):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], []

    for s in sentences:
        words = s.split()
        if len(current) + len(words) > max_len:
            chunks.append(" ".join(current))
            current = words
        else:
            current.extend(words)

    if current:
        chunks.append(" ".join(current))
    return chunks


def process_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_chunks = []
    idx = 1

    for item in data:
        raw_text = item.get("content") or ""
        if not raw_text.strip():
            continue

        clean = clean_text(raw_text)
        chunks = chunk_text(clean)

        for ch in chunks:
            if len(ch.split()) < 20:
                continue

            all_chunks.append({
                "id": idx,
                "text": ch,
                "source": item.get("url") or "unknown"
            })
            idx += 1

    return all_chunks


if __name__ == "__main__":
    input_path = Path("data_ssu.json")
    output_path = Path("sgu_prepared.json")

    chunks = process_json(str(input_path))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Подготовлено {len(chunks)} чанков")
