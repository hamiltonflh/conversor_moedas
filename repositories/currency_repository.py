import requests

class CurrencyRepository:
    @staticmethod
    def fetch_conversion_rate(moeda1, moeda2):
        """Fetch the conversion rate from the external API."""
        api = f"https://economia.awesomeapi.com.br/json/last/{moeda1.upper()}-{moeda2.upper()}"
        response = requests.get(api)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    @staticmethod
    def fetch_historical_data(moeda1, moeda2, dias):
        """Fetch historical data for the given currency pair."""
        api = f"https://economia.awesomeapi.com.br/json/daily/{moeda1.upper()}-{moeda2.upper()}/{dias}"
        response = requests.get(api)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()