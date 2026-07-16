import json
import re
from pathlib import Path
from tqdm import tqdm

RAW_DIR = Path("raw")
OUT_DIR = Path("processed")

OUT_DIR.mkdir(exist_ok=True)

# -------------------------
# DLL blacklist
# -------------------------

DLL_NAMES = {
    "kernel32",
    "kernel32.dll",
    "advapi32",
    "advapi32.dll",
    "user32",
    "user32.dll",
    "shell32",
    "shell32.dll",
    "ntdll",
    "ntdll.dll",
    "gdi32",
    "gdi32.dll",
    "ole32",
    "ole32.dll",
    "oleaut32",
    "crypt32",
    "crypt32.dll",
    "ws2_32",
    "ws2_32.dll",
    "wininet",
    "wininet.dll",
    "urlmon",
    "urlmon.dll"
}

# -------------------------
# metadata words
# -------------------------

BAD_WORDS = {
    "api number",
    "example",
    "frequency",
    "count",
    "description",
    "index",
    "total",
    "api no",
    "number"
}

API_REGEX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_valid_api(token):

    if token is None:
        return False

    token = str(token).strip()

    if token == "":
        return False

    lower = token.lower()

    if lower in DLL_NAMES:
        return False

    for word in BAD_WORDS:
        if word in lower:
            return False

    if not API_REGEX.match(token):
        return False

    return True


files = list(RAW_DIR.rglob("*.json"))

print(f"Found {len(files)} files")

removed = 0
kept = 0

for file in tqdm(files):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    apis = data.get("critical_api_calls", [])

    cleaned = []

    for api in apis:

        if is_valid_api(api):
            cleaned.append(api)
            kept += 1
        else:
            removed += 1

    data["critical_api_calls"] = cleaned

    out_file = OUT_DIR / file.relative_to(RAW_DIR)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

print("\nCleaning Complete")
print("Kept   :", kept)
print("Removed:", removed)