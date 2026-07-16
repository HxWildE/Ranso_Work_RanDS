import json
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

DATASET = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")

types = defaultdict(set)

for file in tqdm(DATASET.rglob("*.json")):

    try:
        with open(file, encoding="utf-8") as f:
            d = json.load(f)

        for k, v in d.items():
            types[k].add(type(v).__name__)

    except:
        pass

print()

for k in sorted(types):
    print(k)
    print("   ", types[k])