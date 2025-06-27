from pathlib import Path
import pyarrow.dataset as ds   # pip install pyarrow>=14

# ── folder that holds the 47 part_XX.parquet files ──────────────────────────
PARQUET_DIR = Path("../filtered_tweets")   # adjust if you run from repo root

# sanity-check: show how many files we see
parts = sorted(PARQUET_DIR.glob("part_*.parquet"))
print(f"Found {len(parts)} Parquet files.")

# ── count rows per file without loading data ────────────────────────────────
total_rows = 0
for pfile in parts:
    n = ds.dataset(pfile, format="parquet").count_rows()   # footer-only scan
    print(f"{pfile.name:<18} {n:>10,} tweets")
    total_rows += n

print("-" * 32)
print(f"GRAND TOTAL          {total_rows:>10,} tweets")
