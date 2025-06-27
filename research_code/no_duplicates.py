import duckdb, pathlib

ROOT = pathlib.Path("../filtered_tweets")   # adjust if you’re in repo root

# 1️⃣ Build a new Parquet dataset that
#     – keeps only UNIQUE tweet ids
#     – drops anything whose text starts with "RT @"
duckdb.sql(f"""
    COPY (
        SELECT DISTINCT *
        FROM read_parquet('{ROOT}/*.parquet')
        WHERE NOT lower(rawContent) LIKE 'rt @%%'
    )
    TO '{ROOT}/no_retweets' (FORMAT PARQUET, COMPRESSION ZSTD);
""")

# 2️⃣ How many survived?
n = duckdb.sql(f"SELECT COUNT(*) FROM read_parquet('{ROOT}/no_retweets')").fetchone()[0]
print(f"Non-RT unique tweets: {n:,}")
