import re

from embeddings.indexer import collection, model


def _tokenize(text):
    return set(re.findall(r"[a-z0-9_]+", text.lower()))


def _keyword_score(query, document):
    query_lower = query.lower().strip()
    doc_lower = document.lower()

    score = 0
    if query_lower and query_lower in doc_lower:
        score += 10

    query_tokens = _tokenize(query)
    doc_tokens = _tokenize(document)
    score += len(query_tokens & doc_tokens)

    return score


def role_based_search(query, user_role):
    user_role = (user_role or "").lower().strip()
    query_embedding = model.encode(query).tolist()

    role_access = {
        "employee": ["employee", "general"],
        "hr": ["hr", "employee", "general"],
        "finance": ["finance", "employee", "general"],
        "engineering": ["engineering", "employee", "general"],
        "marketing": ["marketing", "employee", "general"],
        "c_level": None
    }

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": 8
    }

    if user_role != "c_level":
        allowed_roles = role_access.get(user_role, ["employee", "general"])
        query_args["where"] = {"role": {"$in": allowed_roles}}

    results = collection.query(**query_args)

    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    ranked = sorted(
        zip(docs, metadatas, distances, ids),
        key=lambda item: (_keyword_score(query, item[0]), -(1 - item[2])),
        reverse=True
    )

    if not ranked:
        return results

    results["documents"][0] = [item[0] for item in ranked]
    results["metadatas"][0] = [item[1] for item in ranked]
    results["distances"][0] = [item[2] for item in ranked]
    results["ids"][0] = [item[3] for item in ranked]
    return results
