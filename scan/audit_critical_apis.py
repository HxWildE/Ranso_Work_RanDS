import json
import re
import statistics
from pathlib import Path
from collections import Counter
from tqdm import tqdm
import csv

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

DATASET = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")
OUTPUT = Path("audit_output")
OUTPUT.mkdir(exist_ok=True)

# ---------------------------------------------------
# Counters
# ---------------------------------------------------

total_files = 0
files_with_api = 0
files_without_api = 0

total_api_calls = 0

sequence_lengths = []

api_counter = Counter()

garbage_counter = Counter()

identifier_regex = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# ---------------------------------------------------
# Scan
# ---------------------------------------------------

for file in tqdm(DATASET.rglob("*.json")):

    total_files += 1

    try:

        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        apis = data.get("critical_api_calls", [])

        length = len(apis)

        sequence_lengths.append(length)

        if length == 0:
            files_without_api += 1
            continue

        files_with_api += 1

        total_api_calls += length

        for api in apis:

            api = str(api).strip()

            api_counter[api] += 1

            if not identifier_regex.match(api):
                garbage_counter[api] += 1

    except Exception:
        continue

# ---------------------------------------------------
# Statistics
# ---------------------------------------------------

avg_len = statistics.mean(sequence_lengths)
median_len = statistics.median(sequence_lengths)
max_len = max(sequence_lengths)
min_len = min(sequence_lengths)

sorted_lengths = sorted(sequence_lengths)

p95 = sorted_lengths[int(len(sorted_lengths) * 0.95)]

coverage = files_with_api / total_files * 100

# ---------------------------------------------------
# Console Summary
# ---------------------------------------------------

print("\n" + "="*60)
print("DATASET SUMMARY")
print("="*60)

print(f"Total JSON files          : {total_files}")
print(f"Files with APIs           : {files_with_api}")
print(f"Files without APIs        : {files_without_api}")
print(f"Coverage                 : {coverage:.2f}%")

print()

print(f"Total API calls           : {total_api_calls}")
print(f"Unique APIs               : {len(api_counter)}")

print()

print(f"Average sequence length   : {avg_len:.2f}")
print(f"Median sequence length    : {median_len}")
print(f"Maximum                  : {max_len}")
print(f"Minimum                  : {min_len}")
print(f"95 Percentile            : {p95}")

# ---------------------------------------------------
# Top APIs
# ---------------------------------------------------

print("\n" + "="*60)
print("TOP 50 APIS")
print("="*60)

for api, freq in api_counter.most_common(50):
    print(f"{api:35} {freq}")

# ---------------------------------------------------
# Rare APIs
# ---------------------------------------------------

rare = [(a, c) for a, c in api_counter.items() if c <= 2]

print("\nRare APIs :", len(rare))

# ---------------------------------------------------
# Sequence Distribution
# ---------------------------------------------------

distribution = Counter(sequence_lengths)

# ---------------------------------------------------
# Save top APIs
# ---------------------------------------------------

with open(OUTPUT / "top_apis.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow(["API", "Frequency"])

    for api, freq in api_counter.most_common():
        writer.writerow([api, freq])

# ---------------------------------------------------
# Save Rare APIs
# ---------------------------------------------------

with open(OUTPUT / "rare_apis.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow(["API", "Frequency"])

    for api, freq in sorted(rare):
        writer.writerow([api, freq])

# ---------------------------------------------------
# Save Length Distribution
# ---------------------------------------------------

with open(OUTPUT / "sequence_distribution.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow(["SequenceLength", "Samples"])

    for length in sorted(distribution):
        writer.writerow([length, distribution[length]])

# ---------------------------------------------------
# Save Garbage
# ---------------------------------------------------

with open(OUTPUT / "garbage_tokens.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow(["Token", "Frequency"])

    for token, freq in garbage_counter.most_common():
        writer.writerow([token, freq])

# ---------------------------------------------------
# Save Stats
# ---------------------------------------------------

stats = {
    "total_files": total_files,
    "files_with_api": files_with_api,
    "files_without_api": files_without_api,
    "coverage_percent": coverage,
    "total_api_calls": total_api_calls,
    "unique_apis": len(api_counter),
    "average_sequence_length": avg_len,
    "median_sequence_length": median_len,
    "maximum_sequence_length": max_len,
    "minimum_sequence_length": min_len,
    "95_percentile": p95,
    "rare_api_count": len(rare),
}

with open(OUTPUT / "dataset_stats.json", "w") as f:
    json.dump(stats, f, indent=4)

print("\nSaved all reports to:", OUTPUT.resolve())