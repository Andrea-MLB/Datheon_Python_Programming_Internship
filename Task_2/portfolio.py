import csv
import os
import random
from datetime import datetime

# Try to import yfinance for live prices
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("Note: 'yfinance' not installed. Using simulated prices for demonstration.")


def load_valid_tickers(filename="dataset.txt"):
    """Reads dataset.txt to get a set of valid S&P 500 tickers."""
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            return {row["Symbol"].strip() for row in csv.DictReader(file)}
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Ticker validation will be skipped.")
        return set()


def get_current_price(ticker, buy_price):
    """Returns (price, source). Live via yfinance, else a simulated price."""
    if HAS_YFINANCE:
        try:
            return round(float(yf.Ticker(ticker).fast_info["last_price"]), 2), "live"
        except Exception:
            pass  # API/network problem -> fall through to simulation

    # random.Random(ticker) is repeatable (hash() changes every run), and
    # the price stays within +/-20% of the buy price so returns are realistic.
    return round(buy_price * random.Random(ticker).uniform(0.8, 1.2), 2), "sim"


def main():
    print("=== Investment Portfolio Tracker ===")
    valid_tickers = load_valid_tickers()
    portfolio = {}  # ticker -> {"shares": ..., "buy_price": ...}

    # 1. Gather user input
    while True:
        ticker = input("\nEnter stock ticker (or press Enter to finish): ").upper().strip()
        if not ticker:
            break

        # reject tickers that are not in the dataset
        if valid_tickers and ticker not in valid_tickers:
            print(f"'{ticker}' is not in the S&P 500 dataset. Try again.")
            continue

        try:
            shares = float(input(f"Enter number of shares for {ticker}: "))
            buy_price = float(input(f"Enter buy price per share for {ticker}: $"))
        except ValueError:
            print("Invalid input! Please enter numeric values for shares and price.")
            continue

        #same ticker twice -> merge using a weighted-average buy price
        if ticker in portfolio:
            old = portfolio[ticker]
            total_shares = old["shares"] + shares
            buy_price = (old["shares"] * old["buy_price"] + shares * buy_price) / total_shares
            shares = total_shares

        portfolio[ticker] = {"shares": shares, "buy_price": buy_price}
        print(f"Holding in {ticker}: {shares:.2f} shares @ ${buy_price:.2f} average.")

    if not portfolio:
        print("No portfolio data entered. Exiting.")
        return

    # 2. Calculate valuations
    summary_data = []
    total_invested = total_current_value = 0.0
    any_simulated = False

    print("\n" + "=" * 90)
    print(f"{'Ticker':<8} | {'Shares':<8} | {'Buy Price':<10} | {'Current':<10} | "
          f"{'Gain/Loss':<12} | {'Return %':<9} | Src")
    print("-" * 90)

    for ticker, data in portfolio.items():
        shares, buy_price = data["shares"], data["buy_price"]
        current_price, source = get_current_price(ticker, buy_price)
        any_simulated = any_simulated or source == "sim"

        invested = shares * buy_price
        current_value = shares * current_price
        gain_loss = current_value - invested
        pct_change = (gain_loss / invested) * 100 if invested > 0 else 0

        total_invested += invested
        total_current_value += current_value

        print(f"{ticker:<8} | {shares:<8.2f} | ${buy_price:<9.2f} | ${current_price:<9.2f} | "
              f"${gain_loss:<11.2f} | {pct_change:<8.2f}% | {source}")

        summary_data.append({
            "Ticker": ticker, "Shares": shares, "Buy Price": round(buy_price, 2),
            "Current Price": round(current_price, 2), "Total Invested": round(invested, 2),
            "Current Value": round(current_value, 2), "Gain/Loss": round(gain_loss, 2),
            "Percentage": round(pct_change, 2), "Price Source": source,
        })

    print("-" * 90)
    total_gain_loss = total_current_value - total_invested
    total_pct = (total_gain_loss / total_invested) * 100 if total_invested > 0 else 0

    print(f"TOTAL INVESTED:  ${total_invested:,.2f}")
    print(f"TOTAL VALUE:     ${total_current_value:,.2f}")
    print(f"TOTAL GAIN/LOSS: ${total_gain_loss:,.2f} ({total_pct:.2f}%)")
    if any_simulated:
        print("Note: 'sim' prices are simulated (yfinance unavailable), not real market data.")

    # append to the CSV (timestamped) instead of overwriting it
    csv_filename = "portfolio_summary.csv"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fieldnames = ["Timestamp", "Ticker", "Shares", "Buy Price", "Current Price",
                  "Total Invested", "Current Value", "Gain/Loss", "Percentage", "Price Source"]
    try:
        new_file = not os.path.exists(csv_filename)
        with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if new_file:
                writer.writeheader()
            for row in summary_data:
                writer.writerow({"Timestamp": stamp, **row})
            writer.writerow({"Timestamp": stamp, "Ticker": "TOTAL",
                             "Total Invested": round(total_invested, 2),
                             "Current Value": round(total_current_value, 2),
                             "Gain/Loss": round(total_gain_loss, 2),
                             "Percentage": round(total_pct, 2)})
        print(f"\nSuccess! Portfolio summary saved to '{csv_filename}'.")
    except Exception as e:
        print(f"\nError saving to CSV: {e}")


if __name__ == "__main__":
    main()