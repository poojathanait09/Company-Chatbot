import os

import pandas as pd


def load_markdown(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".md"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                docs.append({
                    "text": f.read(),
                    "source": file
                })
    return docs


def load_csv(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            for _, row in df.iterrows():
                docs.append({
                    "text": str(row.to_dict()),
                    "source": file
                })
    return docs


def load_documents(folder):
    docs = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            department = root.split(os.sep)[-1].lower()

            if file.endswith(".md"):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    docs.append({
                        "text": f.read(),
                        "source": file,
                        "department": department
                    })

            elif file.endswith(".csv"):
                df = pd.read_csv(path)
                for _, row in df.iterrows():
                    row_dict = {k: str(v) for k, v in row.to_dict().items()}
                    row_text = " | ".join([f"{k}: {v}" for k, v in row_dict.items()])
                    docs.append({
                        "text": row_text,
                        "source": file,
                        "department": department,
                        "row_data": row_dict
                    })

    return docs
