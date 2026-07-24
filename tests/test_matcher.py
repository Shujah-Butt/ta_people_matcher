import pandas as pd # type: ignore

from matcher import find_matches


def test_duplicate_email_match():

    applicants = pd.DataFrame([
        {
            "applicant_id": "A001",
            "full_name": "Ali Khan",
            "email": "ali@gmail.com",
            "phone": "",
            "cnic": "",
            "city": "Lahore",
            "role": "Developer",
            "applied_on": "2025-01-01"
        }
    ])

    employees = pd.DataFrame([
        {
            "employee_id": "E001",
            "employee_name": "Ali Khan",
            "personal_email": "ALI@gmail.com",
            "cell_number": "",
            "cnic": "",
            "status": "Active",
            "date_of_joining": "2024-01-01"
        }
    ])

    matches, _, _ = find_matches(applicants, employees)

    assert len(matches) == 1
    assert matches.iloc[0]["confidence"] == "High"


def test_missing_cnic():

    applicants = pd.DataFrame([
        {
            "applicant_id": "A001",
            "full_name": "Ahmed",
            "email": "",
            "phone": "03001234567",
            "cnic": "",
            "city": "",
            "role": "",
            "applied_on": ""
        }
    ])

    employees = pd.DataFrame([
        {
            "employee_id": "E001",
            "employee_name": "Ahmed",
            "personal_email": "",
            "cell_number": "03001234567",
            "cnic": "",
            "status": "Active",
            "date_of_joining": ""
        }
    ])

    matches, _, _ = find_matches(applicants, employees)

    assert len(matches) == 1


def test_phone_variant():

    applicants = pd.DataFrame([
        {
            "applicant_id": "A001",
            "full_name": "Sara",
            "email": "",
            "phone": "+92-300-1234567",
            "cnic": "",
            "city": "",
            "role": "",
            "applied_on": ""
        }
    ])

    employees = pd.DataFrame([
        {
            "employee_id": "E001",
            "employee_name": "Sara",
            "personal_email": "",
            "cell_number": "03001234567",
            "cnic": "",
            "status": "Active",
            "date_of_joining": ""
        }
    ])

    matches, _, _ = find_matches(applicants, employees)

    assert len(matches) == 1


def test_conflict_detection():

    applicants = pd.DataFrame([
        {
            "applicant_id": "A001",
            "full_name": "Muhammad Zia",
            "email": "",
            "phone": "",
            "cnic": "3520212345678",
            "city": "",
            "role": "",
            "applied_on": ""
        },
        {
            "applicant_id": "A002",
            "full_name": "Muhammad Zia",
            "email": "",
            "phone": "",
            "cnic": "3520212345678",
            "city": "",
            "role": "",
            "applied_on": ""
        }
    ])

    employees = pd.DataFrame([
        {
            "employee_id": "E001",
            "employee_name": "Muhammad Zia",
            "personal_email": "",
            "cell_number": "",
            "cnic": "3520212345678",
            "status": "Active",
            "date_of_joining": ""
        }
    ])

    _, _, conflicts = find_matches(applicants, employees)

    assert len(conflicts) == 1