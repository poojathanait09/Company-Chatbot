import re


def clean_text(text):
    text = text.lower().replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("---", "\n")
    text = text.replace("**", "")
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    cleaned_lines = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            cleaned_lines.append("")
            continue

        # Preserve heading titles while removing markdown syntax.
        line = re.sub(r"^\s*#+\s*", "", line)
        # Strip ordered-list numbering at line start without touching decimals.
        line = re.sub(r"^\s*\d+\.\s+", "", line)
        line = re.sub(r"([a-z])([0-9])", r"\1 \2", line)
        line = re.sub(r"([0-9])([a-z])", r"\1 \2", line)
        line = re.sub(r"[ \t]+", " ", line)
        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)

    if "table of contents" in cleaned:
        cleaned = cleaned.split("table of contents")[-1]

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def extract_sections(text):
    sections = text.split("\n#")
    return sections
