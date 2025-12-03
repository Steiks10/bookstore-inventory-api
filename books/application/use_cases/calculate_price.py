from urllib.error import URLError
from datetime import datetime, timezone

def calculate_suggested_price(cost_usd: float, rate: float, margin_percent: float = 0.0) -> float:
    return float(cost_usd) * float(rate) * (1.0 + (float(margin_percent) / 100.0))

def calculate_price_for_book(repository, rates_provider, book_id: int, currency: str, margin_percent: float = 0.0, save: bool = False):
    dto = repository.get_by_id(book_id)
    if dto is None:
        return None, {"detail": "Libro no encontrado"}

    try:
        payload = rates_provider.fetch_usd_rates()
    except URLError as e:
        return None, {"detail": "Proveedor de tasas no disponible", "error": str(e), "status": 503}
    except Exception as e:
        return None, {"detail": "Error al obtener tasas", "error": str(e), "status": 500}

    rates = payload.get('rates') or {}
    currency = (currency or '').upper().strip()
    if currency not in rates:
        return None, {"detail": f"Moneda no soportada: {currency}", "status": 400}

    rate = float(rates[currency])
    suggested = calculate_suggested_price(dto.cost_usd, rate, margin_percent)
    cost_local = float(dto.cost_usd) * rate

    saved = False
    if save:
        updated = repository.update_by_id(book_id, { 'selling_price_local': suggested })
        saved = updated is not None

    result = {
        'book_id': dto.id,
        'cost_usd': float(dto.cost_usd),
        'exchange_rate': rate,
        'cost_local': cost_local,
        'margin_percentage': float(margin_percent or 0.0),
        'selling_price_local': suggested,
        'currency': currency,
        'calculation_timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }
    return result, None
