# Show Me Exchange Rates

This application downloads and plots exchange rates for different currencies from the European Central Bank (ECB) website.

## Requirements

- Python 3.11
- Packages listed in `Pipfile`

## Installation

1. Clone the repository: git clone https://github.com/Gvolny/show_me.git

2. Navigate to the project directory: cd show_me
3. Install the required packages: pipenv install

4. Activate the virtual environment:pipenv shell


## Usage

1. Run the `main.py` file:
2. Follow the prompts to select the currency you want to view exchange rates for.
3. The application will download the XML file containing exchange rate data for the selected currency and plot the max, min, and mean exchange rates per month.
