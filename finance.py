import csv
import os
import re

import yfinance as yf


def load_tickers_from_file(filename: str) -> list[str]:
    tickers = []
    with open(filename, "r") as file:
        for line in file:
            # Extraer el ticker del URL usando expresiones regulares
            match = re.search(r"quote/([^/]+)/", line)
            if match:
                tickers.append(match.group(1))
    return tickers


# Cargar tickers desde el archivo
tickers = load_tickers_from_file("tickerCol.txt")

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a custom dialect for proper character handling
csv.register_dialect(
    "custom", delimiter=",", quoting=csv.QUOTE_ALL, quotechar='"', lineterminator="\n"
)


def process_ticker(ticker_symbol: str) -> None:
    # Get the ticker data
    data = yf.Ticker(ticker_symbol)
    info_dict = data.info

    # Define the CSV file path using ticker symbol
    csv_file = f"{output_dir}/{ticker_symbol.replace('.', '_')}_info.csv"

    # Write to CSV file
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, dialect="custom")
        # Write header and value rows
        writer.writerow(["Field", "Value"])
        for key, value in info_dict.items():
            # Skip some properties
            if key not in ["companyOfficers", "longBusinessSummary"]:
                writer.writerow([key, value])

    print(f"Data for {ticker_symbol} has been saved to {csv_file}")


# Process each ticker
for ticker in tickers:
    try:
        process_ticker(ticker)
    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")
