from dataclasses import dataclass
from enum import Enum


class CommandShell(str, Enum):
    SHELL = "shell"  # Linux shell
    CMD = "cmd"  # Windows CMD
    POWERSHELL = "powershell"


@dataclass(frozen=True)
class Command:
    command: str
    shell: CommandShell
