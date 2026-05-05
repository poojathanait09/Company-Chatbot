import os
import re
from functools import lru_cache

import pandas as pd


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HR_CSV_PATH = os.path.join(BASE_DIR, "data", "Fintech-data", "HR", "hr_data.csv")


@lru_cache(maxsize=1)
def load_hr_data():
    df = pd.read_csv(HR_CSV_PATH)
    df["employee_id_norm"] = df["employee_id"].astype(str).str.lower().str.strip()
    df["role_norm"] = df["role"].astype(str).str.lower().str.strip()
    return df


def _extract_employee_id(query):
    match = re.search(r"\bfinemp\s*-?\s*(\d{4,})\b", query, re.IGNORECASE)
    if not match:
        return None
    return f"finemp{match.group(1)}"


def _format_employee(row):
    return (
        f"Employee {row['employee_id']}: {row['full_name']}\n"
        f"Role: {row['role']}\n"
        f"Department: {row['department']}\n"
        f"Email: {row['email']}\n"
        f"Location: {row['location']}\n"
        f"Date of birth: {row['date_of_birth']}\n"
        f"Date of joining: {row['date_of_joining']}\n"
        f"Manager ID: {row['manager_id']}\n"
        f"Salary: {row['salary']}\n"
        f"Leave balance: {row['leave_balance']}\n"
        f"Leaves taken: {row['leaves_taken']}\n"
        f"Attendance: {row['attendance_pct']}%\n"
        f"Performance rating: {row['performance_rating']}\n"
        f"Last review date: {row['last_review_date']}"
    )


def answer_hr_query(query):
    query_norm = query.lower().strip()
    df = load_hr_data()

    employee_id = _extract_employee_id(query_norm)
    if employee_id:
        match = df[df["employee_id_norm"] == employee_id]
        if not match.empty:
            return _format_employee(match.iloc[0]), "hr_data.csv"

    if "hr manager" in query_norm or "hr managers" in query_norm:
        managers = df[df["role_norm"] == "hr manager"][
            ["employee_id", "full_name", "location", "email", "performance_rating"]
        ].sort_values(["performance_rating", "full_name"], ascending=[False, True])

        if not managers.empty:
            lines = ["HR managers in the company:"]
            for _, row in managers.iterrows():
                lines.append(
                    f"- {row['employee_id']} | {row['full_name']} | {row['location']} | "
                    f"{row['email']} | rating {row['performance_rating']}"
                )
            return "\n".join(lines), "hr_data.csv"

    if "top 5" in query_norm and "salary" in query_norm and "performance" in query_norm:
        top = df.sort_values(["salary", "performance_rating"], ascending=[False, False]).head(5)
        lines = ["Top 5 employees by salary, with performance rating as tie-breaker:"]
        for _, row in top.iterrows():
            lines.append(
                f"- {row['employee_id']} | {row['full_name']} | {row['role']} | "
                f"salary {row['salary']} | rating {row['performance_rating']}"
            )
        return "\n".join(lines), "hr_data.csv"

    return None, None
