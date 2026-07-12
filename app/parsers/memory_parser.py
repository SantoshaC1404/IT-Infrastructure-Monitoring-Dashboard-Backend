def parse_meminfo(raw: str) -> dict:
    result = {}

    for line in raw.splitlines():
        key, value = line.split(":", 1)
        result[key] = int(value.strip().split()[0])

    total = result["MemTotal"]
    available = result["MemAvailable"]
    used = total - available

    return {
        "total_kb": total,
        "used_kb": used,
        "available_kb": available,
        "usage_percent": round((used / total) * 100, 2),
    }
