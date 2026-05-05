from preprocessing.chunker import chunk_text
from preprocessing.cleaner import clean_text
from preprocessing.loader import load_documents
from preprocessing.metadata import assign_metadata


def preprocess(folder):
    raw_docs = load_documents(folder)
    processed_chunks = []
    chunk_id = 0

    for doc in raw_docs:
        clean = clean_text(doc["text"])
        chunks = [clean] if doc["source"].endswith(".csv") else chunk_text(clean)

        for chunk in chunks:
            metadata = assign_metadata(doc)
            processed_chunks.append({
                "id": str(chunk_id),
                "text": chunk,
                "metadata": metadata
            })
            chunk_id += 1

    return processed_chunks
