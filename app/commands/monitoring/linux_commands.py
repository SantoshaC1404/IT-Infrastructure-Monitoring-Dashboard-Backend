from app.dto.command.command_dto import Command
from app.commands.monitoring.base import BaseMonitoringCommandSet
from app.utils.enums import CommandShell


class LinuxMonitoringCommandSet(BaseMonitoringCommandSet):

    # CPU Usage
    def cpu_usage(self):
        return Command(
            "top -bn1 | awk '/Cpu\\(s\\)/ {print 100-$8}'",
            CommandShell.SHELL,
        )

    # Memory Usage
    def memory_usage(self):
        return Command(
            "free | grep Mem | awk '{print $3/$2 * 100.0}'",
            CommandShell.SHELL,
        )

    # Disk Usage
    def disk_usage(self):
        return Command(
            "df / | tail -1 | awk '{print $5}' | tr -d '%'",
            CommandShell.SHELL,
        )

    # Network Usage
    def network_usage(self):
        return Command(
            "cat /proc/net/dev | grep ':'",
            CommandShell.SHELL,
        )

    # Uptime
    def uptime(self):
        return Command(
            "cat /proc/uptime | cut -d'.' -f1",
            CommandShell.SHELL,
        )

    # Load Average
    def load_average(self):
        return Command(
            "cat /proc/loadavg | awk '{print $1}'",
            CommandShell.SHELL,
        )

    # Process Count
    def process_count(self):
        return Command(
            "ps -e --no-headers | wc -l",
            CommandShell.SHELL,
        )

    # Current Logged In User
    def current_logged_in_user(self):

        return Command(
            command="last -F | head -1",
            shell=CommandShell.SHELL,
        )

    # Last Login Time
    def last_login(self):

        return Command(
            command="last -F | head -1",
            shell=CommandShell.SHELL,
        )
