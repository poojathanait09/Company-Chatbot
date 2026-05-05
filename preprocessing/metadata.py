def assign_metadata(doc):
    dept = doc["department"].lower().strip()

    role_map = {
        "finance": "finance",
        "hr": "hr",
        "engineering": "engineering",
        "marketing": "marketing",
        "general": "general"
    }

    metadata = {
        "department": dept,
        "role": role_map.get(dept, "general"),
        "source": doc["source"]
    }

    row_data = doc.get("row_data") or {}
    if row_data.get("employee_id"):
        metadata["employee_id"] = str(row_data["employee_id"]).lower()
    if row_data.get("full_name"):
        metadata["full_name"] = str(row_data["full_name"]).lower()

    return metadata
