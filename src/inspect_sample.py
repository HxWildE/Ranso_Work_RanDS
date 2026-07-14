import json
from pathlib import Path

# Change this path after locating one JSON file
DATASET_ROOT = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")

# Find the first JSON recursively
json_files = list(DATASET_ROOT.rglob("*.json"))

print(f"Found {len(json_files)} JSON files.")

if not json_files:
    raise Exception("No JSON files found!")

sample = json_files[0]

print("\nOpening:")
print(sample)

with open(sample, "r", encoding="utf-8") as f:
    data = json.load(f)

print("\n========== KEYS ==========\n")

for key in data.keys():
    print(key)

print("\n==========================\n")

print("Data types:\n")

for key, value in data.items():
    print(f"{key:<30} {type(value).__name__}")

print("\n==========================\n")

if "critical_api_calls" in data:

    apis = data["critical_api_calls"]

    print(f"Total API calls: {len(apis)}")

    print("\nFirst 20 APIs:\n")

    for api in apis[:20]:
        print(api)

else:
    print("critical_api_calls NOT FOUND!")













# Open ONE JSON
# ↓
# Print keys
# ↓
# Print types
# ↓
# Print critical_api_calls length
# ↓
# Print first few API calls
# ↓
# Exit