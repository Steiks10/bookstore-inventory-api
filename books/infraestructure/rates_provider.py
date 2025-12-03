import json
from urllib.request import urlopen
from urllib.error import URLError
from ..domain.rates import RatesProvider

class HttpRatesProvider(RatesProvider):
    def fetch_usd_rates(self):
        with urlopen('https://api.exchangerate-api.com/v4/latest/USD', timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
