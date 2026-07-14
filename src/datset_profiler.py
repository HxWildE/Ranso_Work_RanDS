import os
import json
import random
from collections import Counter, defaultdict
from statistics import mean, median

from tqdm import tqdm

# ==========================================================
# CONFIG
# ==========================================================

DATASET_ROOT = r"data/raw/RanDS_Behaviour_Activity_Dataset/dataset"

# Number of APIs to display randomly
RANDOM_API_COUNT = 10

# Number of longest samples to print
TOP_LONGEST = 10

# ==========================================================
# VARIABLES
# ==========================================================

total_json = 0
json_errors = 0
missing_api_key = 0
empty_sequences = 0

api_counter = Counter()

sequence_lengths = []

# (length, filepath)
longest_sequences = []

prefix_counter = Counter()

sample_sequence = None

PREFIXES = [
    "Nt",
    "Zw",
    "Create",
    "Open",
    "Get",
    "Set",
    "Reg",
    "Crypt",
    "Write",
    "Read",
]

# ==========================================================
# SCAN DATASET
# ==========================================================

print("\nScanning dataset...\n")

for root, dirs, files in os.walk(DATASET_ROOT):

    for file in files:

        if not file.endswith(".json"):
            continue

        total_json += 1

        path = os.path.join(root, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        except Exception:
            json_errors += 1
            continue

        if "apis" not in data:
            missing_api_key += 1
            continue

        apis = data["apis"]

        if len(apis) == 0:
            empty_sequences += 1
            continue

        if sample_sequence is None:
            sample_sequence = apis

        L = len(apis)

        sequence_lengths.append(L)

        longest_sequences.append((L, path))

        for api in apis:

            api_counter[api] += 1

            for p in PREFIXES:
                if api.startswith(p):
                    prefix_counter[p] += 1
                    break

# ==========================================================
# REPORT
# ==========================================================

print("\n" + "=" * 70)
print("DATASET PROFILE")
print("=" * 70)

print(f"Total JSON files          : {total_json}")
print(f"Unreadable JSON           : {json_errors}")
print(f"Missing API key           : {missing_api_key}")
print(f"Empty API sequences       : {empty_sequences}")
print(f"Valid samples             : {len(sequence_lengths)}")

print()

print(f"Unique APIs               : {len(api_counter)}")
print(f"Total API Calls           : {sum(api_counter.values())}")

print()

print("SEQUENCE LENGTHS")
print("----------------")

print(f"Minimum                   : {min(sequence_lengths)}")
print(f"Maximum                   : {max(sequence_lengths)}")
print(f"Average                   : {mean(sequence_lengths):.2f}")
print(f"Median                    : {median(sequence_lengths)}")

# ==========================================================
# HISTOGRAM
# ==========================================================

bins = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6-10": 0,
    "11-20": 0,
    "21-50": 0,
    "51-100": 0,
    "101+": 0,
}

for L in sequence_lengths:

    if L == 1:
        bins["1"] += 1
    elif L == 2:
        bins["2"] += 1
    elif L == 3:
        bins["3"] += 1
    elif L == 4:
        bins["4"] += 1
    elif L == 5:
        bins["5"] += 1
    elif L <= 10:
        bins["6-10"] += 1
    elif L <= 20:
        bins["11-20"] += 1
    elif L <= 50:
        bins["21-50"] += 1
    elif L <= 100:
        bins["51-100"] += 1
    else:
        bins["101+"] += 1

print()
print("=" * 70)
print("SEQUENCE LENGTH DISTRIBUTION")
print("=" * 70)

for k, v in bins.items():
    print(f"{k:10s}: {v}")

# ==========================================================
# API FREQUENCY DISTRIBUTION
# ==========================================================

freq_bins = defaultdict(int)

for freq in api_counter.values():

    if freq == 1:
        freq_bins["1"] += 1
    elif freq <= 5:
        freq_bins["2-5"] += 1
    elif freq <= 10:
        freq_bins["6-10"] += 1
    elif freq <= 50:
        freq_bins["11-50"] += 1
    elif freq <= 100:
        freq_bins["51-100"] += 1
    elif freq <= 500:
        freq_bins["101-500"] += 1
    else:
        freq_bins["500+"] += 1

print()
print("=" * 70)
print("API FREQUENCY DISTRIBUTION")
print("=" * 70)

for k in ["1", "2-5", "6-10", "11-50", "51-100", "101-500", "500+"]:
    print(f"{k:10s}: {freq_bins[k]}")

# ==========================================================
# TOP APIs
# ==========================================================

print()
print("=" * 70)
print("TOP 30 APIs")
print("=" * 70)

for api, cnt in api_counter.most_common(30):
    print(f"{api:40s} {cnt}")

# ==========================================================
# RANDOM APIs
# ==========================================================

print()
print("=" * 70)
print(f"{RANDOM_API_COUNT} RANDOM APIs")
print("=" * 70)

random_apis = random.sample(
    list(api_counter.keys()),
    min(RANDOM_API_COUNT, len(api_counter))
)

for api in random_apis:
    print(api)

# ==========================================================
# PREFIXES
# ==========================================================

print()
print("=" * 70)
print("API PREFIX COUNTS")
print("=" * 70)

for p in PREFIXES:
    print(f"{p:10s}: {prefix_counter[p]}")

# ==========================================================
# LONGEST SEQUENCES
# ==========================================================

print()
print("=" * 70)
print(f"TOP {TOP_LONGEST} LONGEST SAMPLES")
print("=" * 70)

longest_sequences.sort(reverse=True)

for length, path in longest_sequences[:TOP_LONGEST]:
    print(f"{length:5d}  {path}")

# ==========================================================
# SAMPLE SEQUENCE
# ==========================================================

print()
print("=" * 70)
print("FIRST NON-EMPTY SAMPLE")
print("=" * 70)

if sample_sequence:

    for api in sample_sequence[:100]:
        print(api)

    if len(sample_sequence) > 100:
        print("...")

print("\nProfiling complete.")