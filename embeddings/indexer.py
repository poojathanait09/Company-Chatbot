import os

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.getenv("CHROMA_DB_PATH", os.path.join(BASE_DIR, "chroma_db_runtime"))
COLLECTION_NAME = "company_data"
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def resolve_model_path():
    explicit_path = os.getenv("EMBEDDING_MODEL_PATH")
    if explicit_path:
        return explicit_path

    cached_snapshot = os.path.join(
        os.path.expanduser("~"),
        ".cache",
        "huggingface",
        "hub",
        "models--sentence-transformers--all-MiniLM-L6-v2",
        "snapshots",
        "c9745ed1d9f207416be6d2e6f8de32d1f16199bf",
    )

    if os.path.exists(cached_snapshot):
        return cached_snapshot

    return DEFAULT_MODEL_NAME


os.makedirs(DB_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=DB_PATH)
model = SentenceTransformer(resolve_model_path(), local_files_only=True)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def reset_collection():
    global collection

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def store_chunks(chunks, batch_size=64):
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        documents = [chunk["text"] for chunk in batch]
        embeddings = model.encode(documents).tolist()
        metadatas = [chunk["metadata"] for chunk in batch]
        ids = [chunk["id"] for chunk in batch]

        collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
