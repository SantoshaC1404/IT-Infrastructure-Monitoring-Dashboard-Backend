from app.services.ssh_service import SSHService


class LinuxCollector:

    def __init__(self, ssh: SSHService):
        self.ssh = ssh

    def read_file(self, path: str) -> str:
        return self.ssh.execute(f"cat {path}")

    def cpu(self):
        return self.read_file("/proc/stat")

    def memory(self):
        return self.read_file("/proc/meminfo")

    def load(self):
        return self.read_file("/proc/loadavg")

    def uptime(self):
        return self.read_file("/proc/uptime")

    def network(self):
        return self.read_file("/proc/net/dev")

    def mounts(self):
        return self.read_file("/proc/mounts")

    def os_release(self):
        return self.read_file("/etc/os-release")

    def disk_usage(self):
        return self.ssh.execute("df -B1P")
