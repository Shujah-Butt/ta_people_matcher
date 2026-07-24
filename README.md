# ta_people_matcher

A lightweight Python tool that helps HR teams safely match applicant records with employee records during HR system migration.

This project was developed as part of the TechAbout Python Developer Assessment.

---

# Features

- Normalize CNIC, email, phone numbers, and names
- Match applicants to employees using:
  1. Exact CNIC
  2. Exact Email
  3. Exact Phone
  4. Name Similarity (RapidFuzz)
- Assign confidence levels:
  - High
  - Medium
  - Low
- Prevent multiple employees from being automatically matched to one applicant
- Generate audit-ready reports

---

# Project Structure

```
ta_people_matcher/
│
├── outputs/
│   ├── matches.csv
│   ├── unmatched_applicants.csv
│   ├── conflicts.csv
│   └── summary.json
│
├── sample_data/
│   ├── applicants.csv
│   └── employees.csv
│
├── tests/
│   ├── test_normalizer.py
│   └── test_matcher.py
│
├── app.py
├── matcher.py
├── models.py
├── normalizer.py
├── utils.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Installation

Create a virtual environment

```bash
python -m venv venv
```

Activate it

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run

```bash
python app.py
```

---

# Run Tests

```bash
python -m pytest
```

---

# Matching Rules

The application matches records in the following order:

1. Exact CNIC
2. Exact Email
3. Exact Phone
4. Name Similarity (>=90%)

Priority is important because CNIC is considered the strongest identifier, followed by email and phone.

---

# Confidence Levels

| Confidence | Rule |
|------------|------|
| High | Exact CNIC or Email Match |
| Medium | Exact Phone Match |
| Low | Name Similarity |

Each match also contains a reason explaining why it was selected.

---

# Conflict Handling

The application never silently matches multiple applicants to the same employee.

Instead, it creates a conflict record for manual HR review.

---

# Tests

The project includes tests for:

- CNIC normalization
- Email normalization
- Phone normalization
- Duplicate emails
- Missing CNIC
- Phone format variations
- Name matching
- Conflict detection

---

# Design Decisions

- Exact identifiers are preferred over fuzzy matching.
- Name similarity is only used as a fallback.
- Outputs are fully auditable through confidence levels and reason strings.
- The solution prioritizes reducing false positives over maximizing automatic matches.

---

# Future Improvements

- FastAPI interface
- Interactive web dashboard
- Configurable similarity threshold
- PostgreSQL support
- Logging framework
- Docker deployment

---

Developed for the TechAbout Python Developer Assessment.