import requests
import os
from lxml import etree


def save_xml(currency):
    # check if folder exists
    folder = "currency"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = f"{folder}/{currency}.xml"
    response = requests.get(
        f"https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/{currency}.xml"
    )
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        print("Error while downloading XML file")


def get_list_of_currencies():
    url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"

    response = requests.get(url)
    if response.status_code == 200:
        root = etree.HTML(response.content)
        currencies = root.xpath('//table[@class="forextable"]//a[@href]/text()')

        while "\n" in currencies:
            currencies.remove("\n")
        currency_dict = {
            currencies[i]: currencies[i + 1] for i in range(0, len(currencies), 2)
        }
        return currency_dict

    else:
        print("Error while parsing list of available currencies")
