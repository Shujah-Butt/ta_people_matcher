import json
import os

import pandas as pd # type: ignore

from matcher import find_matches


INPUT_FOLDER = "sample_data"
OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

applicants = pd.read_csv(
    f"{INPUT_FOLDER}/applicants.csv"
)

employees = pd.read_csv(
    f"{INPUT_FOLDER}/employees.csv"
)

matches, unmatched, conflicts = find_matches(
    applicants,
    employees,
)

matches.to_csv(
    f"{OUTPUT_FOLDER}/matches.csv",
    index=False,
)

unmatched.to_csv(
    f"{OUTPUT_FOLDER}/unmatched_applicants.csv",
    index=False,
)

conflicts.to_csv(
    f"{OUTPUT_FOLDER}/conflicts.csv",
    index=False,
)

from datetime import datetime

summary = {
    "total_applicants": len(applicants),
    "matched": len(matches),
    "unmatched": len(unmatched),
    "conflicts": len(conflicts),
    "high_confidence": len(matches[matches["confidence"] == "High"]),
    "medium_confidence": len(matches[matches["confidence"] == "Medium"]),
    "low_confidence": len(matches[matches["confidence"] == "Low"]),
    "generated_at": datetime.now().isoformat(timespec="seconds")
}

with open(
    f"{OUTPUT_FOLDER}/summary.json",
    "w"
) as f:

    json.dump(summary, f, indent=4)

print("Done!")
print(summary)