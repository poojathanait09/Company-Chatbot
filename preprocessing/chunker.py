import re


def _split_large_paragraph(paragraph, chunk_size):
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
    chunks = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        candidate = f"{current} {sentence}".strip()
        if current and len(candidate) > chunk_size:
            chunks.append(current.strip())
            current = sentence
        else:
            current = candidate

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_text(text, chunk_size=900):
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    chunks = []
    current_chunk = ""

    for block in blocks:
        if len(block) > chunk_size:
            large_parts = _split_large_paragraph(block, chunk_size)
        else:
            large_parts = [block]

        for part in large_parts:
            candidate = f"{current_chunk}\n\n{part}".strip() if current_chunk else part
            if current_chunk and len(candidate) > chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = part
            else:
                current_chunk = candidate

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
