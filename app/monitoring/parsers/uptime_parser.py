def parse_uptime(raw: str) -> int:
    return int(float(raw.split()[0]))
