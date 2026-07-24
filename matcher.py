import pandas as pd # type: ignore
from rapidfuzz import fuzz # type: ignore

from normalizer import (
    normalize_name,
    normalize_email,
    normalize_phone,
    normalize_cnic,
)


def preprocess(df, is_employee=False):
    df = df.copy()

    if is_employee:
        df["name"] = df["employee_name"].apply(normalize_name)
        df["email"] = df["personal_email"].apply(normalize_email)
        df["phone"] = df["cell_number"].apply(normalize_phone)
    else:
        df["name"] = df["full_name"].apply(normalize_name)
        df["email"] = df["email"].apply(normalize_email)
        df["phone"] = df["phone"].apply(normalize_phone)

    df["cnic"] = df["cnic"].apply(normalize_cnic)

    return df


def find_matches(applicants, employees):

    applicants = preprocess(applicants)
    employees = preprocess(employees, True)

    matches = []
    unmatched = []
    conflicts = []

    used_employee_ids = set()

    for _, app in applicants.iterrows():

        match = None
        confidence = ""
        reason = ""

        # ----------------------------
        # 1. Exact CNIC
        # ----------------------------

        if app["cnic"]:

            result = employees[
                employees["cnic"] == app["cnic"]
            ]

            if len(result) == 1:

                match = result.iloc[0]
                confidence = "High"
                reason = "Exact CNIC Match"

        # ----------------------------
        # 2. Exact Email
        # ----------------------------

        if match is None and app["email"]:

            result = employees[
                employees["email"] == app["email"]
            ]

            if len(result) == 1:

                match = result.iloc[0]
                confidence = "High"
                reason = "Exact Email Match"

        # ----------------------------
        # 3. Exact Phone
        # ----------------------------

        if match is None and app["phone"]:

            result = employees[
                employees["phone"] == app["phone"]
            ]

            if len(result) == 1:

                match = result.iloc[0]
                confidence = "Medium"
                reason = "Exact Phone Match"

        # ----------------------------
        # 4. Name Similarity
        # ----------------------------

        if match is None:

            best_score = 0
            best_row = None

            for _, emp in employees.iterrows():

                score = fuzz.ratio(
                    app["name"],
                    emp["name"]
                )

                if score > best_score:
                    best_score = score
                    best_row = emp

            if best_score >= 90:

                match = best_row
                confidence = "Low"
                reason = f"Name Similarity ({best_score}%)"

        # ----------------------------
        # Conflict Detection
        # ----------------------------

        if match is not None:

            emp_id = match["employee_id"]

            if emp_id in used_employee_ids:

                conflicts.append({
                    "applicant_id": app["applicant_id"],
                    "employee_id": emp_id,
                    "confidence": confidence,
                    "match_reason": reason,
                    "conflict_reason": "Employee matched to multiple applicants"
                })

            else:

                used_employee_ids.add(emp_id)

                matches.append({

                    "applicant_id": app["applicant_id"],
                    "employee_id": emp_id,
                    "confidence": confidence,
                    "reason": reason

                })

        else:

            unmatched.append(app.to_dict())

    return (
        pd.DataFrame(matches),
        pd.DataFrame(unmatched),
        pd.DataFrame(conflicts),
    )