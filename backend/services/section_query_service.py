import os
import re
from functools import lru_cache


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data", "Fintech-data")


ROLE_FOLDERS = {
    "employee": ["general"],
    "engineering": ["engineering", "general"],
    "finance": ["finance", "general"],
    "hr": ["hr", "general"],
    "marketing": ["marketing", "general"],
    "c_level": None,
}


def _normalize(text):
    text = text.lower()
    text = re.sub(r"^\s*\d+(?:\.\d+)*\.?\s*", "", text)
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _parse_sections(lines):
    headings = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        match = re.match(r"^(#+)\s+(.*)$", stripped)
        if match:
            headings.append({
                "index": idx,
                "level": len(match.group(1)),
                "heading": match.group(2).strip(),
            })

    sections = []
    for pos, heading in enumerate(headings):
        end = len(lines)
        for next_heading in headings[pos + 1:]:
            if next_heading["level"] <= heading["level"]:
                end = next_heading["index"]
                break

        content_lines = lines[heading["index"] + 1:end]
        sections.append({
            "heading": heading["heading"],
            "content": content_lines,
        })

    return sections


@lru_cache(maxsize=1)
def _load_sections():
    sections = []

    for root, _, files in os.walk(DATA_DIR):
        department = os.path.basename(root).lower()

        for file in files:
            if not file.endswith(".md"):
                continue

            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                lines = handle.read().splitlines()

            for section in _parse_sections(lines):
                sections.append({
                    "department": department,
                    "source": file,
                    "heading": section["heading"],
                    "heading_norm": _normalize(section["heading"]),
                    "content": section["content"],
                })

    return sections


def answer_section_query(query, role):
    query_norm = _normalize(query)
    if not query_norm:
        return None, None

    allowed = ROLE_FOLDERS.get(role, ["general"])
    candidates = []

    for section in _load_sections():
        if allowed is not None and section["department"] not in allowed:
            continue

        heading_norm = section["heading_norm"]
        content_text = "\n".join([line for line in section["content"] if line.strip()]).strip()
        content_norm = _normalize(content_text)

        score = 0
        if query_norm == heading_norm:
            score += 100
        if heading_norm and heading_norm in query_norm:
            score += 60
        if query_norm and query_norm in heading_norm:
            score += 50

        overlap = len(set(query_norm.split()) & set(heading_norm.split()))
        score += overlap * 5

        if query_norm in content_norm:
            score += 10

        if score > 0 and content_text:
            candidates.append((score, section["heading"], content_text, section["source"]))

    if not candidates:
        return None, None

    candidates.sort(key=lambda item: item[0], reverse=True)
    _, heading, content, source = candidates[0]
    return f"{heading}\n{content}".strip(), source
