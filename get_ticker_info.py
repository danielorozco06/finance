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
    for directory in ["input/tickers_info", "input/tickers_history"]:
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


def save_ticker_history(ticker_symbol: str) -> None:
    data = yf.Ticker(ticker_symbol)
    csv_file = f"input/tickers_history/{ticker_symbol.replace('.', '_')}_values.csv"
    data.history(period="6mo").to_csv(csv_file)
    print(f"Historical data for {ticker_symbol} has been saved to {csv_file}")


def main() -> None:
    tickers = load_tickers_from_file("tickerCol.txt")
    setup_directories()

    for ticker in tickers:
        try:
            save_ticker_info(ticker)
            save_ticker_history(ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")


if __name__ == "__main__":
    main()
