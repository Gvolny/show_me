from scrapper import get_dict_of_currencies


def print_available_currencies():
    currencies = get_dict_of_currencies()
    print("This app can download and plot exchange rates for the following currencies:")
    for key, value in currencies.items():
        print(f"{key}: {value}")
