# Betting on Democracy: Investigating How Kalshi’s 2024 Presidential Prediction Market Shaped Online Discourse and May Have Influenced Voter Behavior

<img src="https://github.com/user-attachments/assets/20a89972-af31-4212-b270-1fdf06be0c7e" alt="Image 1" width="480" />
<img src="https://github.com/user-attachments/assets/14eb92fc-8fa1-4e93-a55a-be75b955b768" alt="Image 1" width="170" />
<img src="https://github.com/user-attachments/assets/11092de4-fd8a-4664-bc02-cc3e102acf4e" alt="Image 1" width="170" />

<br>

## This repository documents a research project exploring whether legalized betting on the U.S. presidential election affected online discourse. The project analyzes Twitter/X and TikTok posts alongside historical betting data from the Kalshi API.

<img src="https://github.com/user-attachments/assets/2cac393b-aa70-40f0-ac95-382b1f95d421" alt="Image 1" width="170" />
<img src="https://github.com/user-attachments/assets/c1b88803-2ead-465a-a717-5b35e6a59301" alt="Image 2" width="150" />

## Project Overview

The 2024 U.S. presidential race marked the first modern cycle in which retail investors could
legally wager on the outcome through Kalshi’s “Yes‑No” political futures contracts. While
proponents frame the market as an information‑aggregation tool, critics argue that real‑money
stakes may distort civic intent, incentivizing individuals to vote, or persuade others to vote,
solely to maximize financial gain. This project investigates whether participation in Kalshi’s
presidential markets measurably influenced online discourse and, by extension, voter behavior.
Using large‑scale social‑media datasets from X/Twitter and TikTok, combined with Kalshi’s
historical order‑book API, we will (1) quantify gambling‑related election engagement, (2) model
temporal correlations between market movements and partisan messaging, and (3) evaluate the
possibility of coordinated amplification by campaign‑adjacent actors, including Donald Trump Jr.
Findings will contribute to the literature on election integrity and inform regulatory debates
surrounding prediction markets.

## Project Abstract

The 2024 U.S. presidential election was the first in modern history to allow everyday Americans to wager legally on the outcome via Kalshi’s “Yes‑No” political futures contracts. While advocates claim such markets merely aggregate information, critics warn that real‑money stakes could warp the civic motivations behind voting and influence public opinion. This study examines whether—and how—participation in Kalshi’s presidential market altered online engagement and, by extension, voter behavior. Leveraging large‑scale datasets from X/Twitter and TikTok (2019‑2024) alongside Kalshi’s historical order‑book API, we will:

1. Quantify the volume and sentiment of gambling‑related election discourse over time.

2. Model temporal links between Kalshi price swings and surges in partisan messaging.

3. Detect signs of strategic amplification by campaign‑adjacent figures, including Donald Trump Jr., who served as a Kalshi adviser.

Using causal‑inference techniques (Granger causality, difference‑in‑differences) and bot‑detection heuristics, we aim to determine whether financial incentives measurably nudged political persuasion online. Findings will inform the broader debate on prediction‑market regulation and provide actionable insights for policymakers tasked with safeguarding electoral integrity.

## Project Goals

1. **Collect Data** – Gather election-related tweets and TikTok posts during the 2024 cycle.
2. **Analyze Engagement** – Measure how mentions of betting correlate with candidate support.
3. **Assess Influence** – Investigate whether gambling incentives may have shifted voter behavior or campaign strategies.

## Required Tools

- Python 3.11+
- [Playwright](https://playwright.dev/) for automated browsing
- Pandas and NumPy for data processing
- The [`x-24-us-election`](https://github.com/sinking8/x-24-us-election) x-24-us-election Dataset utility: https://github.com/sinking8/x-24-us-election
- The [`XScraper`](https://github.com/sinking8/XScraper) Twitter scraping utility: https://github.com/sinking8/XScraper
- Access to the Kalshi API for historical betting markets

## Setup Overview

1. Clone the `x-24-us-election` repository and install its dependencies (`pip install -r requirements.txt`).
2. Clone the `XScraper` repository and install its dependencies (`pip install -r requirements.txt` and `playwright install`).
3. Prepare one or more Twitter accounts and save their session cookies as described in the XScraper documentation.
4. Configure a parameter file listing keywords and date ranges to target. Adjust these as your research focus evolves.
5. Run `python app.py --parameters your_parameters.json --output parsed_tweets/output.json` to collect tweets.
6. Query the Kalshi API for market history matching your time frame.

> **Note:** Ensure that any data collection complies with Twitter's Terms of Service and applicable research ethics guidelines.

## Weekly Progress Checklist

Below is a suggested timeline from May 26 through August 2nd (excluding weekends, June 2-6, and July 15‑16).

Tasks Completed/In Progress:
- **Task 1** – Finalize research questions, set up XScraper, API Keys, and Twitter/X 2024 US Election Dataset.
- **Task 2** – Create keyword lists, and begin colelcting data first from Twitter/X 2024 US Election Dataset.
- **Task 3** – Expand keyword lists and run full-scale scraping for the initial time window. Start fetching Kalshi market data.
- **Task 4** – Clean and preprocess Twitter/X.
- **Task 5** – Perform exploratory analysis on engagement metrics and correlate with betting trends.

Future Tasks:
- **Task 1** – Refine analyses, produce visualizations, and begin drafting preliminary findings.
- **Task 2** – Expand project to include other social media platforms such as TikTok, Instagram, Truth Social, etc.
- **Task 3** – Complete all scraping runs and finalize data cleaning steps.
- **Task 3** – Summarize results and prepare any presentations or reports due at the end of the project.

## Data Collected

- Tweets containing election and betting keywords within defined date windows from:
    1. Filtering through Twitter/X 2024 US Election Dataset
    2. Using XScraper
- Kalshi market prices and volumes over the same period

## License

This project uses the MIT License. See the `LICENSE` file for details.
