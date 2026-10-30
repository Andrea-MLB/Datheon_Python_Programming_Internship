---

## Task 2: Investment Portfolio Tracker (Console)

A Python utility to track stock investments, calculate real-time portfolio valuation, and export performance logs to a CSV file.

### Features
* **Data Validation:** Cross-references user input against the provided S&P 500 `dataset.txt` file.
* **Real-Time Valuation:** Calculates total invested capital versus current market value, plus the percentage gain/loss per holding.
* **Live Data + Fallback:** Attempts to use the `yfinance` library for live market prices. If the library is not installed (or the lookup fails), it gracefully falls back to simulated, deterministic prices so the script never crashes.
* **Duplicate Handling:** Buying the same ticker more than once merges the positions using a weighted-average buy price.
* **CSV Export:** Automatically persists the portfolio summary and gain/loss metrics into `portfolio_summary.csv`. Each run appends timestamped rows, building a performance history.
* **Formatted Output:** Clean, aligned console table using Python f-string padding.

### Project Structure
```
Task_2/
├── portfolio.py             # Main script
├── dataset.txt              # S&P 500 constituents (ticker validation)
├── portfolio_summary.csv    # Generated on first run
└── README.md
```

### Requirements
* Python 3.6+
* No external libraries required (uses only `csv`, `os`, `random`, `datetime`)
* *Optional:* `yfinance` for live prices

### How to Run
1. Navigate to the Task 2 directory:
   ```bash
   cd Task_2
   ```
2. *(Optional)* Install `yfinance` for live market prices:
   ```bash
   pip install yfinance
   ```
3. Run the script:
   ```bash
   python3 portfolio.py
   ```
   On Windows, use `python portfolio.py` if `python3` is not recognised.
4. Enter each position when prompted: ticker, number of shares, then buy price. Press **Enter** on an empty ticker to finish.

### Example Session
```
=== Investment Portfolio Tracker ===

Enter stock ticker (or press Enter to finish): AAPL
Enter number of shares for AAPL: 150
Enter buy price per share for AAPL: $10
Holding in AAPL: 150.00 shares @ $10.00 average.

Enter stock ticker (or press Enter to finish): AAPL
Enter number of shares for AAPL: 170
Enter buy price per share for AAPL: $10
Holding in AAPL: 320.00 shares @ $10.00 average.

Enter stock ticker (or press Enter to finish): MSFT
Enter number of shares for MSFT: 300
Enter buy price per share for MSFT: $5
Holding in MSFT: 300.00 shares @ $5.00 average.

Enter stock ticker (or press Enter to finish):

==========================================================================================
Ticker   | Shares   | Buy Price  | Current    | Gain/Loss    | Return %  | Src
------------------------------------------------------------------------------------------
AAPL     | 320.00   | $10.00     | $11.17     | $374.40      | 11.70   % | sim
MSFT     | 300.00   | $5.00      | $4.98      | $-6.00       | -0.40   % | sim
------------------------------------------------------------------------------------------
TOTAL INVESTED:  $4,700.00
TOTAL VALUE:     $5,068.40
TOTAL GAIN/LOSS: $368.40 (7.84%)
Note: 'sim' prices are simulated (yfinance unavailable), not real market data.

Success! Portfolio summary saved to 'portfolio_summary.csv'.
```

### Output File: `portfolio_summary.csv`
| Column | Description |
|---|---|
| Timestamp | When the run happened |
| Ticker | Stock symbol (validated against `dataset.txt`) |
| Shares / Buy Price | Position size and (average) purchase price |
| Current Price | Live or simulated price |
| Total Invested / Current Value | Cost basis vs. current value |
| Gain/Loss / Percentage | Dollar and percentage gain or loss |
| Price Source | `live` (yfinance) or `sim` (simulated) |

Each run also appends a `TOTAL` row with the combined invested capital, current value and overall gain/loss.

### Notes
* **Simulated prices:** When `yfinance` is unavailable, the current price is generated within ±20% of your buy price, seeded by the ticker so the same input always gives the same result. These are **not** real market data, which is why every row is tagged `sim` in both the console and the CSV.
* **Invalid input:** Unknown tickers and non-numeric prices or share counts are rejected with a message, and you are prompted again.
* **Fresh log:** Delete `portfolio_summary.csv` to start a new history.