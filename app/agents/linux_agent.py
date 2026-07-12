from app.services.ssh_service import SSHService


class LinuxAgent:

    def __init__(self, ssh: SSHService):
        self.ssh = ssh

    def hostname(self):
        return self.ssh.execute("hostname")

    def uptime(self):
        return self.ssh.execute("uptime -p")

    def kernel(self):
        return self.ssh.execute("uname -r")

    def cpu_usage(self):
        return self.ssh.execute("top -bn1 | grep 'Cpu(s)'")

    def memory(self):
        return self.ssh.execute("free -m")

    def disk(self):
        return self.ssh.execute("df -h")
