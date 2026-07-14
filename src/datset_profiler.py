from pathlib import Path
from collections import Counter
from tqdm import tqdm
import json
import csv
import random
import statistics

# ---------------- CONFIG ---------------- #

DATASET_ROOT = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")
RESULTS_DIR = Path("results")

# ---------------------------------------- #


def main():

    RESULTS_DIR.mkdir(exist_ok=True)

    json_files = list(DATASET_ROOT.rglob("*.json"))

    print(f"\nFound {len(json_files)} JSON files.\n")

    api_counter = Counter()

    sequence_lengths = []

    random_tokens = []

    total = 0
    empty = 0
    malformed = 0

    for file in tqdm(json_files):

        total += 1

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

        except Exception:
            malformed += 1
            continue

        apis = data.get("critical_api_calls", [])

        if not isinstance(apis, list):
            continue

        sequence_lengths.append(len(apis))

        if len(apis) == 0:
            empty += 1

        for api in apis:

            api = str(api).strip()

            api_counter[api] += 1

            # keep random samples for inspection
            if len(random_tokens) < 100:
                random_tokens.append(api)
            else:
                if random.random() < 0.001:
                    random_tokens[random.randint(0, 99)] = api

    ####################################################
    # Summary
    ####################################################

    non_empty = total - empty

    print("\n========== SUMMARY ==========\n")

    print("Total Samples :", total)
    print("Malformed     :", malformed)
    print("Empty         :", empty)
    print("Non Empty     :", non_empty)

    print()

    print("Vocabulary Size :", len(api_counter))

    print()

    print("Average Length :", round(statistics.mean(sequence_lengths),2))
    print("Median Length  :", statistics.median(sequence_lengths))
    print("Max Length     :", max(sequence_lengths))
    print("Min Length     :", min(sequence_lengths))

    ####################################################
    # Vocabulary
    ####################################################

    with open(RESULTS_DIR/"api_vocabulary.txt","w",encoding="utf-8") as f:

        for api in sorted(api_counter.keys()):
            f.write(api+"\n")

    ####################################################
    # API Frequency
    ####################################################

    with open(RESULTS_DIR/"api_frequency.csv","w",newline="",encoding="utf-8") as f:

        writer=csv.writer(f)

        writer.writerow(["API","Frequency"])

        for api,freq in api_counter.most_common():
            writer.writerow([api,freq])

    ####################################################
    # Sequence Lengths
    ####################################################

    with open(RESULTS_DIR/"sequence_lengths.csv","w",newline="") as f:

        writer=csv.writer(f)

        writer.writerow(["length"])

        for l in sequence_lengths:
            writer.writerow([l])

    ####################################################
    # Random Tokens
    ####################################################

    with open(RESULTS_DIR/"random_api_samples.txt","w",encoding="utf-8") as f:

        for api in sorted(random_tokens):
            f.write(api+"\n")

    ####################################################
    # JSON Summary
    ####################################################

    summary={

        "total_samples":total,

        "malformed":malformed,

        "empty_sequences":empty,

        "non_empty_sequences":non_empty,

        "vocabulary_size":len(api_counter),

        "average_length":statistics.mean(sequence_lengths),

        "median_length":statistics.median(sequence_lengths),

        "max_length":max(sequence_lengths),

        "min_length":min(sequence_lengths)

    }

    with open(RESULTS_DIR/"dataset_summary.json","w") as f:

        json.dump(summary,f,indent=4)

    print("\nDone.\nResults saved inside results/\n")


if __name__=="__main__":
    main()