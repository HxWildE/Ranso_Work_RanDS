import json
from pathlib import Path
from collections import Counter
from tqdm import tqdm

DATASET = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")

key_counter = Counter()
file_count = 0

for file in tqdm(DATASET.rglob("*.json")):
    file_count += 1

    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        key_counter.update(data.keys())

    except Exception:
        continue

print(f"\nFiles scanned : {file_count}\n")

print("Top-level keys:\n")

for k, v in key_counter.most_common():
    print(f"{k:35} {v}")