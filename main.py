import embeddings.indexer as indexer
from preprocessing.pipeline import preprocess


def rebuild_index():
    chunks = preprocess("data/Fintech-data")
    print(f"Prepared {len(chunks)} chunks")

    indexer.reset_collection()
    indexer.store_chunks(chunks)

    print(f"Indexed {indexer.collection.count()} chunks")


if __name__ == "__main__":
    rebuild_index()
