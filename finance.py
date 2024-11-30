import csv
import os

import yfinance as yf

# List of tickers to process
tickers = ["PFDAVVNDA.CL", "BCOLOMBIA.CL"]

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a custom dialect for proper character handling
csv.register_dialect(
    "custom", delimiter=",", quoting=csv.QUOTE_ALL, quotechar='"', lineterminator="\n"
)


def process_ticker(ticker_symbol):
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
