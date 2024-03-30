import requests
import os
from lxml import etree


def save_xml(currency: str) -> None:
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


def get_dict_of_currencies() -> dict:
    url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"

    response = requests.get(url)
    if response.status_code == 200:
        root = etree.HTML(response.content)
        currencies = root.xpath('//table[@class="forextable"]//tr')[1:]

        currency_dict = {
            i.xpath("./td[1]//text()")[0]: i.xpath("./td[2]//text()")[0]
            for i in currencies
        }
        return currency_dict

    else:
        print("Error while parsing list of available currencies")
