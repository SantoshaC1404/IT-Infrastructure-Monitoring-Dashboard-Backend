class LinuxCollector:

    def collect(self):

        return {
            "cpu": self.cpu(),
            "memory": self.memory(),
            "load": self.load(),
            "uptime": self.uptime(),
            "network": self.network(),
            "disk": self.disk_usage(),
            "os": self.os_release(),
        }
