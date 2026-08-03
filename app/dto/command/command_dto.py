from dataclasses import dataclass

from app.utils.enums import CommandShell


@dataclass(frozen=True)
class Command:
    command: str
    shell: CommandShell
