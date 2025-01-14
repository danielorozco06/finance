import csv
import os
import re

import yfinance as yf


def load_tickers_from_file(filename: str) -> list[str]:
    tickers = []
    with open(filename) as file:
        for line in file:
            if match := re.search(r"quote/([^/]+)/", line):
                tickers.append(match.group(1))
    return tickers


def setup_directories() -> None:
    for directory in ["tickers_history"]:
        os.makedirs(directory, exist_ok=True)


def save_ticker_info(ticker_symbol: str) -> None:
    data = yf.Ticker(ticker_symbol)
    info_dict = {
        k: v
        for k, v in data.info.items()
        if k not in ["companyOfficers", "longBusinessSummary"]
    }

    csv_file = f"input/tickers_info/{ticker_symbol.replace('.', '_')}_info.csv"

    with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Field", "Value"])
        writer.writerows(info_dict.items())

    print(f"Data for {ticker_symbol} has been saved to {csv_file}")


def save_ticker_history(ticker_symbol: str, start_date: str) -> None:
    data = yf.Ticker(ticker_symbol)
    csv_file = f"tickers_history/{ticker_symbol.replace('.', '_')}_values.csv"

    # Get history from start date or using period property with 1d, 5d, 1mo, 3mo, 1y, 5y, max
    history_df = data.history(start=start_date)

    # Keep only desired columns
    history_df = history_df[["Open", "Close", "Volume", "High", "Low"]]
    history_df.to_csv(csv_file)
    print(f"Historical data for {ticker_symbol} has been saved to {csv_file}")


def main() -> None:
    tickers = load_tickers_from_file("input/tickerCol.txt")
    setup_directories()

    for ticker in tickers:
        try:
            # save_ticker_info(ticker)
            save_ticker_history(ticker, start_date="2022-01-01")
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")


if __name__ == "__main__":
    main()
