from dataclasses import dataclass


@dataclass
class CpuStat:
    user: int
    nice: int
    system: int
    idle: int
    iowait: int
    irq: int
    softirq: int
    steal: int


def parse_cpu(raw: str) -> CpuStat:
    values = raw.splitlines()[0].split()[1:]

    return CpuStat(
        user=int(values[0]),
        nice=int(values[1]),
        system=int(values[2]),
        idle=int(values[3]),
        iowait=int(values[4]),
        irq=int(values[5]),
        softirq=int(values[6]),
        steal=int(values[7]),
    )
