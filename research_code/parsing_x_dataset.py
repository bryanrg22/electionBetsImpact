import re, itertools
import pathlib
import pandas as pd
from tqdm import tqdm

# 1. Keyword lists -----------------------------------------------------------
KALSHI = [
    "kalshi", "kalshiex", "trade on kalshi",
    "#kalshi", "#kalshimarkets",
    "event contract", "event contracts",
    "kalshi exchange", "kalshi market", 
    "kalshi contract"
]

BET_VERBS = [
    "bet", "betting", "wager", "odds", "chance",
    "line", "spread", "stake",
    "shares", "buy shares", "sell shares",
    "contract", "contracts",
    "gamble", "speculate", "trade", "investment",
    "predict", "prediction", "long", "short", 
    "positions", "yolo", "degens", "trading", "trader"
]

PRICE_TERMS = [
    "price", "price per share", "cost", "value now",
    "payout", "paid out", "payout if win", "payouts",
    "cash out", "exit", "profit", "loss", "return", "apy",
    "entry", "exit", "bid", "ask", "spread", "volatility",
    "premium"
]

POSITION_TERMS = [
    "position", "positions", "open position", "close position",
    "won", "break-even", "hedge", "liquidate",
]

MARKET_TERMS = [
    "market", "markets", "exchange", "liquidity", "volume",
    "price action", "fluctuation", "manipulate the odds", "pump", "dump",
]

# --- compile regex patterns as strings --------------------------------------
TOKEN_SET = list(itertools.chain(
    KALSHI, BET_VERBS, PRICE_TERMS,
    POSITION_TERMS, MARKET_TERMS
))

TOKENS_PATTERN = r"\b(" + "|".join(map(re.escape, TOKEN_SET)) + r")\b"
PRICE_PATTERN = r"\b\d{1,3}(\.\d{1,2})?¢|\b\d{1,2}c\b|\$\d{1,3}(\.\d{1,2})?k?\b"

# 2. Paths & constants -------------------------------------------------------
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "filtered_tweets"
OUTDIR.mkdir(parents=True, exist_ok=True)

CHUNK_COLUMNS = ["id", "epoch", "rawContent", "hashtags", "links", 
                 "retweetCount", "likeCount", "lang", "user"]
CHUNK_SIZE = 50_000
hits = []
current_part = None

def matching_mask(series: pd.Series) -> pd.Series:
    text = series.str.lower().fillna("")
    mask1 = text.str.contains(TOKENS_PATTERN, regex=True, case=False)
    mask2 = text.str.contains(PRICE_PATTERN, regex=True, case=False)
    return mask1 | mask2

# 3. Stream through every .csv.gz -------------------------------------------
for csv_gz in tqdm(list(ROOT.glob("part_*/*.csv.gz"))):
    part_id = csv_gz.parent.name

    # Flush buffer when changing parts
    if part_id != current_part and hits:
        try:
            full_df = pd.concat(hits)
            # Convert ID to string to avoid integer overflow
            full_df["id"] = full_df["id"].astype(str)
            full_df.to_parquet(OUTDIR / f"{current_part}.parquet",
                               index=False, compression="zstd")
        except Exception as e:
            print(f"Error writing {current_part}.parquet: {e}")
        hits.clear()
    current_part = part_id

    try:
        # Read with explicit dtype specification
        for df in pd.read_csv(
            csv_gz,
            compression="gzip",
            usecols=CHUNK_COLUMNS,
            dtype={"id": str},  # Force ID to string
            dtype_backend="pyarrow",
            chunksize=CHUNK_SIZE,
            low_memory=False
        ):
            # Ensure ID remains string type
            df["id"] = df["id"].astype(str)
            
            mask = matching_mask(df["rawContent"])
            if mask.any():
                hits.append(df.loc[mask])
                
    except Exception as e:
        print(f"Error processing {csv_gz}: {e}")
        continue

# 4. Final flush -------------------------------------------------------------
if hits:
    try:
        full_df = pd.concat(hits)
        full_df["id"] = full_df["id"].astype(str)
        full_df.to_parquet(OUTDIR / f"{current_part}.parquet",
                           index=False, compression="zstd")
    except Exception as e:
        print(f"Error in final flush: {e}")