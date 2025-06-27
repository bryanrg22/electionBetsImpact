#!/usr/bin/env python3
"""Count tweets mentioning Kalshi-related terms in Parquet files.

Usage:
    python count_kalshi_mentions.py [PARQUET_DIR]

The script scans all ``*.parquet`` files in ``PARQUET_DIR`` (default: ``filtered_tweets``)
for tweets containing Kalshi keywords and prints the total count.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import duckdb  # type: ignore
except Exception as e:  # pragma: no cover - optional dependency not present
    raise SystemExit("duckdb is required to run this script") from e

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


def build_regex() -> str:
    """Return a case-insensitive regex that matches any keyword."""
    tokens = "|".join(re.escape(k) for k in MARKET_TERMS)
    return rf"(?i)\b({tokens})\b"


def count_matches(parquet_dir: Path) -> int:
    """Return number of rows matching the regex across all Parquet files."""
    pattern = build_regex()
    query = f"""
        SELECT COUNT(*)
        FROM read_parquet('{parquet_dir.as_posix()}/*.parquet')
        WHERE regexp_matches(rawContent, '{pattern}')
    """
    return duckdb.sql(query).fetchone()[0]



directory = Path("../filtered_tweets")
if not directory.exists():
    raise SystemExit(f"Directory not found: {directory}")
total = count_matches(directory)
print(f"MARKET_TERMS keyword tweets: {total:,}")