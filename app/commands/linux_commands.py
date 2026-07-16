from app.commands.base import BaseCommandSet


class LinuxCommandSet(BaseCommandSet):

    def cpu_usage(self):
        return "top -bn1 | grep 'Cpu(s)' | awk '{print 100-$8}'"

    def memory_usage(self):
        return "free | grep Mem | awk '{print $3/$2 * 100.0}'"

    def disk_usage(self):
        return "df / | tail -1 | awk '{print $5}' | tr -d '%'"

    def network_usage(self):
        return "cat /proc/net/dev | grep ':'"

    def uptime(self):
        return "cat /proc/uptime | cut -d'.' -f1"

    def load_average(self):
        return "cat /proc/loadavg | awk '{print $1}'"

    def process_count(self):
        return "ps -e --no-headers | wc -l"
