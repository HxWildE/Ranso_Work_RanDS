import json
from pathlib import Path
from collections import Counter
from tqdm import tqdm

DATASET = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")

non_empty = Counter()

for file in tqdm(DATASET.rglob("*.json")):

    try:
        with open(file, encoding="utf-8") as f:
            d = json.load(f)

        for k, v in d.items():

            ok = False

            if isinstance(v, list):
                ok = len(v) > 0

            elif isinstance(v, dict):
                ok = len(v) > 0

            elif isinstance(v, str):
                ok = v.strip() != ""

            elif v is not None:
                ok = True

            if ok:
                non_empty[k] += 1

    except:
        pass

print()

for k, v in non_empty.most_common():
    print(f"{k:35} {v}")