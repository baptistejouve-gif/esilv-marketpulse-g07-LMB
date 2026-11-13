 feature/display-market-info

from pathlib import Path

main
import csv
import json
from pathlib import Path

DATA_DIR = Path("data/sample")

def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)

def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]

def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]

def get_first_close(prices):
    return float(prices[0]["close"])

def get_last_close(prices):
    return float(prices[-1]["close"])
feature/display-market-info


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]

 main


def display_market_summary(asset, prices, show_currency=True):
    print(f"{asset['ticker']} - {asset['name']}")
    
    # --- NOUVELLES LIGNES POUR LE TD05 ---
    if "market" in asset:
        print(f"Market       : {asset['market']}")
    if "currency" in asset:
        print(f"Currency     : {asset['currency']}")
    # -------------------------------------
        
    print(f"Observations : {len(prices)}")
    
    first_date = get_first_date(prices)
    last_date = get_last_date(prices)
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)
feature/display-market-metadata
    
    currency_str = f" {asset.get('currency', '')}" if show_currency else ""
    
    print(f"First date   : {first_date}")
    print(f"Last date    : {last_date}")
    print(f"First close  : {first_close:.2f}{currency_str}")
    print(f"Last close   : {last_close:.2f}{currency_str}\n")


    print(f'{asset["ticker"]} - {asset["name"]}')
feature/display-market-info
    print(f'Market : {asset["market"]}')

    if "market" in asset:
        print(f'Market       : {asset["market"]}')
    if "currency" in asset:
        print(f'Currency     : {asset["currency"]}')
 main
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")

    if show_currency:
        print(f'First close  : {first_close:.2f} {asset["currency"]}')
        print(f'Last close   : {last_close:.2f} {asset["currency"]}')
    else:
        print(f"First close  : {first_close:.2f}")
        print(f"Last close   : {last_close:.2f}")

main

def main():
    print("=== MarketPulse ===\n")
    
    instruments = load_instruments()
    prices = load_prices()
    
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]
    
    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])
    
    print("Market configuration")
    print("Period   : 1 month")
    print("Interval : Daily\n")
    
    print("Instrument")
    display_market_summary(instrument, instrument_prices, show_currency=True)
    
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)

if __name__ == "__main__":
    main()
