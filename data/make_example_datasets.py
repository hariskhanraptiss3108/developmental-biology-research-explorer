"""Generates data/example_datasets.csv.

EVERY NUMBER IN THE CSV IS INVENTED by this script (random numbers with a fixed seed).
None of it comes from a real experiment. Run it with:  python data/make_example_datasets.py
"""
import csv
import random
from pathlib import Path

rng = random.Random(2024)
rows = []


def add_group(scenario, group, n, mean, sd, prefix):
    for i in range(1, n + 1):
        rows.append([scenario, group, f"{prefix}{i:02d}", round(max(0.1, rng.gauss(mean, sd)), 1)])


# Scenario 1: tissue size, two separate groups of fictional embryos
add_group("tissue_size", "Control", 12, 100, 9, "C")
add_group("tissue_size", "Reduced gene activity", 12, 91, 10, "R")

# Scenario 2: cell growth in two fictional culture conditions (8 wells each)
add_group("cell_growth", "Condition A", 8, 100, 12, "A")
add_group("cell_growth", "Condition B", 8, 128, 15, "B")

# Scenario 3: same 10 fictional specimens measured at 24 h and 48 h (paired)
for i in range(1, 11):
    early = round(max(50, rng.gauss(180, 20)), 1)
    gain = rng.gauss(85, 25)
    rows.append(["paired_feature", "24 h", f"S{i:02d}", early])
    rows.append(["paired_feature", "48 h", f"S{i:02d}", round(early + gain, 1)])

# Zebrafish case study (fictional): tissue size, control vs reduced gene activity
add_group("zebrafish_case", "Control", 14, 100, 10, "C")
add_group("zebrafish_case", "Reduced gene activity", 14, 80, 14, "G")

out = Path(__file__).with_name("example_datasets.csv")
with out.open("w", newline="") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(["scenario", "group", "subject_id", "value"])
    writer.writerows(rows)
print(f"Wrote {len(rows)} rows to {out}")
