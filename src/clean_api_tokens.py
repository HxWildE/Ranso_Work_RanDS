import re
import json
import csv
from pathlib import Path
from tqdm import tqdm

DATASET_ROOT = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")
RESULTS_DIR = Path("results")

# Windows API naming pattern
API_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def classify(token):

    token = token.strip()

    if token == "":
        return "EMPTY"

    if token.startswith("#"):
        return "NUMBER"

    if token.startswith("{"):
        return "PLACEHOLDER"

    if ".exe" in token.lower():
        return "EXE"

    if "\\" in token or "/" in token:
        return "PATH"

    if "::" in token:
        return "DOTNET"

    if "." in token:
        return "JAVA_OR_DOT"

    if token.lower().endswith("32"):
        return "DLL"

    if API_PATTERN.fullmatch(token):
        return "API"

    return "OTHER"


def main():

    counts = {}

    examples = {}

    for file in tqdm(DATASET_ROOT.rglob("*.json")):

        with open(file,"r",encoding="utf-8") as f:
            data = json.load(f)

        for token in data.get("l",[]):

            category = classify(str(token))

            counts[category] = counts.get(category,0)+1

            if category not in examples:
                examples[category]=token

    print("\n===== TOKEN TYPES =====\n")

    for k,v in sorted(counts.items(),key=lambda x:x[1],reverse=True):

        print(f"{k:15} {v:8}   Example : {examples[k]}")

    RESULTS_DIR.mkdir(exist_ok=True)

    with open(RESULTS_DIR/"token_categories.csv","w",newline="",encoding="utf-8") as f:

        writer=csv.writer(f)

        writer.writerow(["Category","Count","Example"])

        for k,v in sorted(counts.items(),key=lambda x:x[1],reverse=True):

            writer.writerow([k,v,examples[k]])


if __name__=="__main__":
    main()