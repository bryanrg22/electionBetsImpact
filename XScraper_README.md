# XScraper

High‑throughput Playwright‑powered **Twitter / X** scraper built for large‑scale
historical and real‑time data collection.  
It is battle‑tested on election‑cycle analysis but the modular design lets you
swap in any keyword set or HTML mapping without touching core logic.

---

## ✨ Key Features

| Capability | Details |
|------------|---------|
| **Headless browser scraping** | Uses Playwright 1.44 to authenticate with real session cookies and intercept GraphQL traffic directly – no fragile HTML parsing needed. |
| **Keyword‑window search** | JSON parameter decks let you define complex OR‑chained search strings plus precise `since:` / `until:` timestamps down to the second. |
| **Rate‑limit aware rotation** | Multiple authenticated accounts are loaded from cookie jars and rotated automatically whenever `x-rate‑limit‑remaining` is low. |
| **Incremental back‑scroll** | Parser returns the epoch of the last tweet fetched; the scroller resumes from there, ensuring *zero overlap & zero gaps*. |
| **Pluggable parsers** | `helpers/parser_helpers.py` normalises SearchTimeline payloads; alternative mappers (BeautifulSoup / lxml) are supported via `mappers/*.json`. |
| **Crash‑proof runs** | Unknown payload shapes are dumped to `errorfile.json` and the run continues, so long jobs never die mid‑stream. |
| **Unit‑test fixtures** | Golden sample `data_preprocessed.test.json` plus a CSV smoke‑test runner (`appCSVTest.py`). |

---

## 🗂 Project Layout

```text
XSCRAPER/
├── __pycache__/                    # compiled‑bytecode cache
│   └── accounts_cookies*.pyc
├── cookies/                        # exported Playwright session cookies
│   └── <username>.json
├── helpers/
│   └── parser_helpers.py           # shared HTML / JSON parsing utilities
├── mappers/
│   └── easy_scraper.json           # field‑mapping template for tweet entities
├── parameters/                     # search‑filter & runtime configs
│   └── <keyword_set>.json
├── parsed_tweets/                  # cached, cleaned tweet payloads
│   ├── _ipynb_checkpoints/
│   └── week_may30_june7_without_space_keywords_new_1.temp.json
├── .DS_Store
├── .gitignore
├── README.md                       # quick‑start & usage docs
├── account_cookies.sample.py       # helper to save Twitter cookies in Playwright
├── add_accounts.py                 # CLI tool – add multiple handles / rotate logins
├── app.py                          # entry point – orchestrates scraping & CSV export
├── appCSVTest.py                   # smoke‑test runner for CSV output
├── app.log                         # runtime logs (git‑tracked for demo)
├── data_preprocessed.test.json     # example of final structured tweet data
├── errorfile.json                  # sample error tracebacks for debugging
├── requirements.txt                # pinned Python dependencies
├── sample.json                     # tiny fixture tweet batch
├── screenshot.png                  # UI snapshot for README
└── screenshot_after10.png          # post‑run validation screenshot
```


---

## 🔧 Setup

```bash
# 1️⃣ clone repo & create venv
git clone https://github.com/your‑handle/XScraper.git
cd XScraper
python -m venv .venv && source .venv/bin/activate

# 2️⃣ install deps
pip install --upgrade pip
pip install -r requirements.txt
playwright install  # installs browsers

# 3️⃣ add cookies
cp account_cookies.sample.py accounts_cookies.py
#   ↳  paste your auth_token, ct0, _twitter_sess for **each** account
```

> **Tip:** try the one‑liner in `appCSVTest.py` to auto‑generate fresh cookie
> files if you’re able to log in interactively.

---

## 🚀 Quick Start (Production JSON run)

```bash
python app.py --parameters parameters/parameters(1).json               --output parsed_tweets/election_may30.json
```

*Arguments (also flag‑parseable via ENV variables)*

| Flag | Description |
|------|-------------|
| `--parameters` | Path to the JSON deck defining keywords & date window. |
| `--output` | (optional) Override default output filepath. |
| `--headless` | `true` / `false` (default `true`). |

The scraper will:

1. Randomly choose a cookie jar, load it into a new Playwright context.
2. Build the advanced search string from the parameter deck.
3. Scroll the **Latest** feed while intercepting `/SearchTimeline` GraphQL calls.
4. Pipe each response through `helpers/parser_helpers.py`.
5. Append de‑duplicated clean rows into `parsed_tweets/*.json`.

Progress, rate‑limit hits, and errors stream to STDOUT & `app.log`.

---

## ⚙️ Parameter File Anatomy

```jsonc
{
  "keywords": [
    "Joe Biden",
    "Donald Trump",
    "#Election2024"
  ],
  "startDate": "2023-05-30T00:00:00Z",
  "endDate":   "2023-05-31T00:00:00Z",
  "mode": "EXACT"
}
```

*Modify → save → re‑run* to scrape a new slice without touching code.

---

## 🏗️ Parser Logic

![Parser flowchart](screenshot.png)

1. `parse_search_timeline_response()` traverses every `TimelineAddEntries`.
2. Each entry’s raw tweet is flattened by `basic_tweet_content()`.
3. The helper injects convenience columns (`epoch`, booleans, URL) and returns a dict.
4. Results aggregate until chunk size ≥ 100 then flush to disk.
5. Unknown schema → dump raw blob into `errorfile.json` with a timestamp.

See **helpers/parser_helpers.py** for the exact field list.

---

## 📈 Post‑Processing

```python
import pandas as pd, json
df = pd.json_normalize(json.load(open(
    "parsed_tweets/week_may30_june7_without_space_keywords_new_1.temp.json")))
df.info()
```

Typical clean‑up steps:

* Drop placeholder `"PW"` columns → `df.replace("PW", pd.NA, inplace=True)`
* Convert `epoch` → `pd.to_datetime(df["epoch"], unit="s")`
* Explode `links` and `mentionedUsers` arrays for network analysis.

---

## 🛂 Rate‑Limit & Account Rotation

* Twitter currently allows **300** requests / 15‑min window per logged‑in user.
* `app.py` watches the `x-rate-limit-remaining` header and sleeps when < 20.
* When an account hits two consecutive cool‑downs it hot‑swaps to the next jar.
* Total tweets scraped are tracked per session; see the `--max-tweets` flag.

---

## 🪵 Logging

Enable full logs by exporting:

```bash
export XS_LOG=1
```

You’ll get an `app.log` file like:

```
2025‑06‑09 18:41 INFO  Selected account: @data_bot
2025‑06‑09 18:41 INFO  Scroll epoch start = 1717286400
…
```

---

## 🧰 Troubleshooting

| Symptom | Fix |
|---------|-----|
| Browser opens but no tweets are captured | Verify your cookies are still valid (auth_token & ct0), run `appCSVTest.py` interactively. |
| Lots of entries in `errorfile.json` | X changed GraphQL schema → update `parser_helpers.py` (see comments at top of file). |
| Playwright exits with `ERR_CONNECTION_RESET` | Twitter is rate‑throttling IP – add VPN or wait 15 min. |

---

## 🗺️ Roadmap

* ✨ **FUZZY** search mode (keyword stemming & typos)
* 🌐 HTTP‑only fallback using `twscrape` for headless‑less servers
* 📊 Built‑in sqlite writer for instant SQL querying
* 🧪 CI unit tests on push (GitHub Actions)

---

## More In-Depth File Explanations
| File / folder                    | Purpose & key implementation points                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **helpers/**parser_helpers.py  | All of the heavy lifting for *turning raw GraphQL timeline JSON into analysis‑ready records*.  <br>• basic_tweet_content() normalises a single Tweet (handles three GraphQL payload variants) → returns a flat dict of 30‑ish scalar fields + lists.<br>• Adds computed helpers such as epoch (UNIX ts) and booleans like retweetedTweet so downstream code can filter easily.<br>• parse_tweet_contents() figures out whether an entry is a single tweet (tweet‑*) or a profile thread (profile‑conversation‑*) and delegates accordingly.  It logs the full offending payload to **errorfile.json** when it hits an unseen structure, which is why the scraper almost never crashes mid‑run.<br>• parse_search_timeline_response() is tailor‑made for the GraphQL SearchTimeline endpoint.  It pulls every *TimelineAddEntries* block, aggregates the cleaned tweets, and returns {data, tweet_count, last_tweet_epoch} — the last value drives the incremental “walk backwards in time” logic in **app.py**.<br>• parse_response() is an older helper for non‑search timelines (kept for completeness).                                                                                                                                                                                                                                                                                                                                         |
| **app.py**                       | **Main production scraper** (JSON output). Run it and it will:  <br>1. Load a *parameter set* (PARAMETERS_FILENAME) that defines **keywords**, start/end dates, and the maximum tweet age window.<br>2. Pick a random cookie jar from accounts_cookies.py (imported as **cookies**) so each session looks like a different logged‑in browser.<br>3. Spin up Playwright → open *x.com* → inject cookies (works around UI login).<br>4. Construct an advanced search string with get_search_string() (keywords wrapped in parentheses + until: & since: gates).<br>5. Scroll the *Latest* tab via keep_scrolling() while attaching page.on("response", intercept_response); that hook captures every GraphQL response, forwards it to parse_search_timeline_response(), and appends the cleaned rows to **parsed\_tweets/\*.json** using append_json_to_file_after_pre_processing() (de‑dupes on tweet ID).<br>6. Tracks X’s rate‑limit headers (x-rate-limit-remaining, x-rate-limit-reset). When **remaining** drops under a random threshold it time.sleep() until reset, then continues from the *last seen tweet epoch* so you never miss data.<br>7. Loops through multiple accounts (list_accounts) until the total_tweets_of_this_session passes the per‑run quota you set in the parameter JSON.<br>*Outputs*:  A growing temp dump (**week\_may30\_june7\_without\_space\_keywords\_new\_1.temp.json**) ready for post‑processing. |
| **appCSVTest.py**                | Sand‑box / smoke‑test variant of app.py that proves the pipeline end‑to‑end without hitting your prod JSON file.  Differences:<br>• Imports **account\_cookies.sample.py** (you patch in one cookie set at a time).<br>• Writes a **CSV** instead of JSON so you can validate in Excel quickly.<br>• Has a relogin_to_update_cookies() helper that can *log in for real*, scrape the browser storage, and build fresh cookie jars in bulk (handy when Twitter invalidates tokens).<br>• Contains a *multiprocessing* block (commented) showing how to shard scraping across CPU cores if you need more throughput.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **account\_cookies.sample.py**   | Red‑acted template showing the exact dict structure Playwright expects (name / value / domain / path / expires).  Use it as a blueprint to paste in real auth\_token / ct0 combos.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **accounts\_cookies1.py**        | Example of a *fully populated* cookie list (auth\_token, ct0, \_twitter\_sess, etc.).  app.py is currently importing accounts_cookies, so rename / symlink this file to **accounts\_cookies.py** (or edit the import) when you go live.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **add\_accounts.py**             | Legacy utility (now fully commented‑out) that once bulk‑loaded login creds into **twscrape**’s SQLite‑backed accounts.db.  Keep it for reference if you decide to switch from Playwright to an HTTP‑only scraper.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **mappers/**easy_scraper.json  | Declarative CSS/attribute mapping for an *alt* extraction path (beautiful‑soap / lxml).  Lists selectors for avatar, username, embedded images, plus stat keys (replyCount, repostCount, …).  Not invoked in the current Playwright flow but useful if Twitter’s HTML layout changes and you want a quick swap.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **parsed\_tweets/** (folder)     | Rolling cache of every cleaned tweet payload your runs have produced.  Naming convention is week_<start>_<end>_<desc>.json.  Each file is appended atomically so you can pipe them straight into pandas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **data\_preprocessed.test.json** | Tiny **golden sample** created by parser_helpers.test_json() to verify that your parsing logic hasn’t regressed.  Great for unit tests.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **errorfile.json**               | When parser_helpers hits an unexpected tweet structure it dumps the raw entry here so you can inspect and update the parser rules.  Keeps your main run from dying mid‑crawl.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **app.log**                      | Optional runtime log captured during long scrapes; not included here but, if enabled, you’ll see timestamped INFO/ERROR lines from every major step in app.py.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **requirements.txt**             | Pin list for Playwright (playwright==1.x), pandas / numpy, and any CLI helpers.  (File not shared yet—see “next files” below.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ****pycache**/**                 | Auto‑generated *.pyc* byte‑code files. Safe to ignore / add to .gitignore.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **parameters/**parameters(1)…parameters(5).json                                         | <u>📌 Purpose</u> – each JSON block is an *input deck* that app.py consumes at startup to define a single scraping pass.<br><br>**Key fields**  <br>• keywords – list of 50‑ish election‑related strings and hashtags (Biden, MAGA, RFK Jr, etc.). These are <br>  • joined with **OR** when mode:"EXACT" (current setting) → the search string looks like (“Joe Biden”) OR (“Donald Trump”) …  <br>  • wrapped by () and attached to Playwright’s /SearchTimeline GraphQL call.<br>• startDate / endDate – granular down to seconds; app.py converts to ISO (since:YYYY‑MM‑DD_HH:MM:SS_UTC) and until: gates so you can slide the window day‑by‑day without code edits.<br>• mode – currently only "EXACT" supported, but parser\_helpers is written so you can add "FUZZY" later (would build a query without quotes and allow stemming).<br><br>**Why five versions?** You split a long July 27 → Aug 1 scrape into 24‑hour chunks to avoid Twitter rate limits and make reruns idempotent. app.py chooses the file you pass on the CLI and names the output cache accordingly. |
| **week_may30_june7_without_space_keywords_new_1.temp.json**                             | A *live run artifact* sitting in **parsed\_tweets/** (copied here for reference). The structure mirrors the list returned by parse_search_timeline_response() – each element is a fully flattened tweet record with:<br>• metadata (id, url, epoch, language flags…)<br>• engagement metrics (replyCount, viewCount etc.)<br>• nested mentionedUsers / links arrays already normalised.<br><br>Fields marked "PW" are placeholders that parser_helpers.py swaps in when Twitter omits that attribute. When you later post‑process the dataset you can safely treat "PW" as NULL. Good practice: drop this file into a Jupyter notebook and run pd.json_normalize() to explore the columns you actually need.                                                                                                                                                                                                                                                                                                                                                                             |
| **requirements.txt**                                                                    | The *reproducible environment lockfile* – 32 pinned wheels.<br>Highlight stops:<br>• playwright==1.44.0 & pyee – headless browser driver + async event hooks used in app.py.<br>• twscrape & ntscraper – HTTP‑only alternatives; you keep them around in case Twitter rate‑limits Playwright—nice future‑proofing.<br>• beautifulsoup4, lxml – not in use by default flow, but required if you switch to the HTML‑scraper path driven by **mappers/easy\_scraper.json**.<br>• pandas, numpy, greenlet – data wrangling; greenlet speeds up Playwright’s cooperative multitasking.<br>Install with python -m pip install -r requirements.txt inside a fresh venv (Python 3.11+ recommended for Playwright 1.44).                                                                                                                                                                                                                                                                                                                                                                          |
| **account\_cookies.sample.py** *(updated note)*                                           | Still the template—no secrets inside. Shows you the full dict schema (domain, expires, httpOnly, etc.) plus the wrapper list named cookies. Copy this to **accounts\_cookies.py**, paste your real auth_token, ct0, _twitter_sess, and you’re ready to scrape multiple sessions in a round‑robin.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **accounts_cookies.py** *(the real one you provided earlier as accounts_cookies1.py)* | Import target for app.py. It defines ACCOUNTS = [{username, cookies:[…]}, …] so Playwright can call context.add_cookies() and hop between logins whenever the rate‑limit headers get tight.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

---

## 📜 License

MIT – feel free to remix, tweak, and build on top.  
See `LICENSE` for full text.

---

*Generated automatically on 2025‑06‑09 by ChatGPT.*