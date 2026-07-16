import json
from pathlib import Path

DATASET = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")

shown = set()

for file in DATASET.rglob("*.json"):

    with open(file, encoding="utf-8") as f:
        d = json.load(f)

    for k, v in d.items():

        if k in shown:
            continue

        if isinstance(v, list) and len(v):

            print("="*80)
            print(k)
            print(v[:2])

            shown.add(k)

        elif isinstance(v, dict) and len(v):

            print("="*80)
            print(k)
            print(v)

            shown.add(k)

    if len(shown) > 30:
        break