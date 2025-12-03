from typing import Dict, Any

class RatesProvider:
    def fetch_usd_rates(self) -> Dict[str, Any]:
        raise NotImplementedError()
