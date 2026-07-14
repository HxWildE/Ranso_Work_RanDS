#checks if the what the dataset advertises is
# actually correct and technically accurate
from pathlib import Path
from collections import Counter
import json
import statistics
from tqdm import tqdm


# ---------------- CONFIG ---------------- #

DATASET_ROOT = Path("data/raw/RanDS_Behaviour_Activity_Dataset/dataset")
RESULTS_DIR = Path("results")

# ---------------------------------------- #


def get_json_files(root: Path):
    """
    Recursively collect every JSON file.
    """
    return list(root.rglob("*.json"))


def validate_dataset(json_files):

    stats = {

        "total_samples": 0,
        "malformed_json": 0,
        "missing_api_key": 0,
        "empty_api_sequences": 0,

    }

    sequence_lengths = []

    api_counter = Counter()

    malformed_files = []

    for file in tqdm(json_files, desc="Scanning Dataset"):

        stats["total_samples"] += 1

        try:

            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

        except Exception:

            stats["malformed_json"] += 1
            malformed_files.append(str(file))

            continue

        # ---------------- API KEY ---------------- #

        if "critical_api_calls" not in data:

            stats["missing_api_key"] += 1
            continue

        apis = data["critical_api_calls"]

        if not isinstance(apis, list):
            continue

        if len(apis) == 0:
            stats["empty_api_sequences"] += 1

        sequence_lengths.append(len(apis))
        api_counter.update(apis)

    return (
        stats,
        sequence_lengths,
        api_counter,
        malformed_files,
    )


def write_report(
    stats,
    sequence_lengths,
    api_counter,
    malformed_files,
):

    RESULTS_DIR.mkdir(exist_ok=True)

    report = RESULTS_DIR / "dataset_report.txt"

    with open(report, "w", encoding="utf-8") as f:

        f.write("========== RanDS DATASET REPORT ==========\n\n")

        f.write(f"Total Samples           : {stats['total_samples']}\n")
        f.write(f"Malformed JSON          : {stats['malformed_json']}\n")
        f.write(f"Missing API Key         : {stats['missing_api_key']}\n")
        f.write(f"Empty API Sequences     : {stats['empty_api_sequences']}\n\n")

        if sequence_lengths:

            f.write("------ Sequence Statistics ------\n")

            f.write(f"Minimum Length          : {min(sequence_lengths)}\n")
            f.write(f"Maximum Length          : {max(sequence_lengths)}\n")
            f.write(f"Average Length          : {statistics.mean(sequence_lengths):.2f}\n")
            f.write(f"Median Length           : {statistics.median(sequence_lengths)}\n\n")

        f.write(f"Unique APIs             : {len(api_counter)}\n\n")

        f.write("------ Top 20 APIs ------\n\n")

        for api, freq in api_counter.most_common(20):
            f.write(f"{api:40} {freq}\n")

        f.write("\n------ Malformed Files ------\n")

        for file in malformed_files:
            f.write(file + "\n")

    print("\nReport written to:\n")
    print(report)


def main():

    print("\nLocating JSON files...\n")

    json_files = get_json_files(DATASET_ROOT)

    print(f"Found {len(json_files)} JSON files.\n")

    (
        stats,
        sequence_lengths,
        api_counter,
        malformed_files,
    ) = validate_dataset(json_files)

    write_report(
        stats,
        sequence_lengths,
        api_counter,
        malformed_files,
    )


if __name__ == "__main__":
    main()