from app.dto.command_dto import Command
from app.commands.monitoring.base import BaseMonitoringCommandSet
from app.utils.enums import CommandShell


class LinuxMonitoringCommandSet(BaseMonitoringCommandSet):

    def cpu_usage(self):
        return Command(
            "top -bn1 | awk '/Cpu\\(s\\)/ {print 100-$8}'",
            CommandShell.SHELL,
        )

    def memory_usage(self):
        # return "free | grep Mem | awk '{print $3/$2 * 100.0}'"
        return Command(
            "free | grep Mem | awk '{print $3/$2 * 100.0}'",
            CommandShell.SHELL,
        )

    def disk_usage(self):
        # return "df / | tail -1 | awk '{print $5}' | tr -d '%'"
        return Command(
            "df / | tail -1 | awk '{print $5}' | tr -d '%'",
            CommandShell.SHELL,
        )

    def network_usage(self):
        # return "cat /proc/net/dev | grep ':'"
        return Command(
            "cat /proc/net/dev | grep ':'",
            CommandShell.SHELL,
        )

    def uptime(self):
        # return "cat /proc/uptime | cut -d'.' -f1"
        return Command(
            "cat /proc/uptime | cut -d'.' -f1",
            CommandShell.SHELL,
        )

    def load_average(self):
        # return "cat /proc/loadavg | awk '{print $1}'"
        return Command(
            "cat /proc/loadavg | awk '{print $1}'",
            CommandShell.SHELL,
        )

    def process_count(self):
        # return "ps -e --no-headers | wc -l"
        return Command(
            "ps -e --no-headers | wc -l",
            CommandShell.SHELL,
        )
