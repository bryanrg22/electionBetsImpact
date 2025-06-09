# Election Betting Influence Research

This repository documents a research project exploring whether legalized betting on the U.S. presidential election affected online discourse. The project analyzes Twitter/X and TikTok posts alongside historical betting data from the Kalshi API.

## Project Goals

1. **Collect Data** – Gather election-related tweets and TikTok posts during the 2024 cycle.
2. **Analyze Engagement** – Measure how mentions of betting correlate with candidate support.
3. **Assess Influence** – Investigate whether gambling incentives may have shifted voter behavior or campaign strategies.

## Required Tools

- Python 3.11+
- [Playwright](https://playwright.dev/) for automated browsing
- Pandas and NumPy for data processing
- The [`XScraper`](https://github.com/sinking8/XScraper) Twitter scraping utility: https://github.com/sinking8/XScraper
- Access to the Kalshi API for historical betting markets

## Setup Overview

1. Clone the `XScraper` repository and install its dependencies (`pip install -r requirements.txt` and `playwright install`).
2. Clone the 
3. Prepare one or more Twitter accounts and save their session cookies as described in the XScraper documentation.
4. Configure a parameter file listing keywords and date ranges to target. Adjust these as your research focus evolves.
5. Run `python app.py --parameters your_parameters.json --output parsed_tweets/output.json` to collect tweets.
6. Query the Kalshi API for market history matching your time frame.

> **Note:** Ensure that any data collection complies with Twitter's Terms of Service and applicable research ethics guidelines.

## Weekly Progress Checklist

Below is a suggested timeline from May 26 through August 2nd (excluding weekends, June 2-6, and July 15‑16).

- **Week 0** – Finalize research questions, set up XScraper, API Keys, and Twitter/X 2024 Election Dataset.
- **Week 1** – Create keyword lists, and begin colelcting data first from Twitter/X 2024 Election Dataset.
- **Week 2** – Expand keyword lists and run full-scale scraping for the initial time window. Start fetching Kalshi market data.
- **Week 3** – Clean and preprocess Twitter/X. Exclude July 15‑16 from scraping jobs.
- **Week 4** – Perform exploratory analysis on engagement metrics and correlate with betting trends.
- **Week 5** – Refine analyses, produce visualizations, and begin drafting preliminary findings.
- **Week 6** – Complete all scraping runs and finalize data cleaning steps.
- **Week 7** – Summarize results and prepare any presentations or reports due at the end of the project.

## Data Collected

- Tweets containing election and betting keywords within defined date windows from:
    1. Filtering through Twitter/X 2024 Election Dataset
    2. Using XScraper
- Kalshi market prices and volumes over the same period

## License

This project uses the MIT License. See the `LICENSE` file for details.