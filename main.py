import argparse
from plot import parse_ecb_exchange_rates, plot_exchange_rates
from scrapper import get_dict_of_currencies, save_xml


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download and plot exchange rates for a specific currency from European Central Bank (ECB)."
    )
    parser.add_argument(
        "--currency", "-c", help='Currency code (e.g., "usd", "pln", "jpy")'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.currency:
        currency = args.currency.lower()
        currencies = None
    else:
        currencies = get_dict_of_currencies()
        print(
            "This app can download and plot exchange rates for the following currencies:"
        )
        for key, value in currencies.items():
            print(f"{key}: {value}")
        currency = input("Enter currency: ").lower()

    currency_list = list(currencies.keys()) if currencies else None
    if currency_list and currency.upper() not in currency_list:
        print("Invalid currency input. Please try again.")
        return
    filename = f"currency/{currency}.xml"
    save_xml(currency)

    df_monthly_max, df_monthly_min, df_monthly_mean = parse_ecb_exchange_rates(filename)
    plot_exchange_rates(
        maximum=df_monthly_max,
        minimum=df_monthly_min,
        mean=df_monthly_mean,
        currency=currency,
    )


if __name__ == "__main__":
    main()
