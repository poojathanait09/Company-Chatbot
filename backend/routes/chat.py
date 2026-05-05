import os
import sys

from fastapi import APIRouter, Depends

# Fix path for direct execution.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.services.hr_query_service import answer_hr_query
from backend.services.section_query_service import answer_section_query
from embeddings.indexer import collection, model
from llm.groq_client import generate_response
from llm.prompt import build_prompt
from rbac import require_role
from search.rbac import role_based_search

router = APIRouter()


def rag_search(query, role):
    query_embedding = model.encode(query).tolist()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=6,
        where={"role": {"$in": [role, "general"]}}
    )


def calculate_confidence(results):
    distances = results.get("distances", [[]])[0]

    if not distances:
        return 0

    score = 1 - min(distances)
    return round(score, 2)


@router.get("/chat")
def chat(query: str, user=Depends(require_role(["employee", "finance", "hr", "engineering", "marketing", "c_level"]))):
    role = user["role"]

    structured_answer, structured_source = answer_hr_query(query)
    if structured_answer and role in ["hr", "c_level"]:
        return {
            "query": query,
            "role": role,
            "answer": structured_answer,
            "source": structured_source,
            "confidence": 1.0
        }

    section_answer, section_source = answer_section_query(query, role)
    if section_answer:
        return {
            "query": query,
            "role": role,
            "answer": section_answer,
            "source": section_source,
            "confidence": 1.0
        }

    results = role_based_search(query, role)

    if not results["documents"][0]:
        return {"answer": "❌ No data found or access restricted"}

    filtered_chunks = [
        (chunk, results["metadatas"][0][i])
        for i, chunk in enumerate(results["documents"][0])
    ]

    context = "\n\n".join([c[0] for c in filtered_chunks[:6]])
    prompt = build_prompt(query, context)
    answer = generate_response(prompt)
    confidence = calculate_confidence(results)

    if confidence < 0.15:
        return {
            "query": query,
            "role": role,
            "answer": "❌ No relevant data found",
            "source": None,
            "confidence": confidence
        }

    if "no relevant data found" in answer.lower():
        return {
            "query": query,
            "role": role,
            "answer": "❌ " + answer if not answer.startswith("❌") else answer,
            "source": None,
            "confidence": 0
        }

    return {
        "query": query,
        "role": role,
        "answer": answer.strip(),
        "source": filtered_chunks[0][1]["source"],
        "confidence": confidence
    }
