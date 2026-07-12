def parse_load(raw: str) -> dict:
    values = raw.split()

    return {
        "load_1m": float(values[0]),
        "load_5m": float(values[1]),
        "load_15m": float(values[2]),
    }
