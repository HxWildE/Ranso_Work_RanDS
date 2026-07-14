import json
from pathlib import Path

DATASET_ROOT = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")

json_files = list(DATASET_ROOT.rglob("*.json"))

print(f"Found {len(json_files)} JSON files.\n")

sample = None
data = None

for file in json_files:

    with open(file, "r", encoding="utf-8") as f:

        temp = json.load(f)

    if len(temp["critical_api_calls"]) > 0:

        sample = file
        data = temp
        break

if sample is None:
    raise Exception("No sample with non-empty critical_api_calls found!")

print("Found first non-empty sample:\n")
print(sample)

print("\nTotal APIs:", len(data["critical_api_calls"]))

print("\nFirst 20 entries:\n")

for x in data["critical_api_calls"][:20]:
    print(repr(x))