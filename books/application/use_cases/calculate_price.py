from urllib.error import URLError

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

    saved = False
    if save:
        updated = repository.update_by_id(book_id, { 'selling_price_local': suggested })
        saved = updated is not None

    result = {
        'book_id': dto.id,
        'currency': currency,
        'rate': rate,
        'base_cost_usd': float(dto.cost_usd),
        'margin_percent': float(margin_percent or 0.0),
        'suggested_price_local': suggested,
        'saved': saved,
    }
    return result, None
