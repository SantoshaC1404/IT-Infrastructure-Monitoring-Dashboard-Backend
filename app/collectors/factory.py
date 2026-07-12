from app.collectors.linux.collector import LinuxCollector
from app.models.server import ServerType


class CollectorFactory:

    @staticmethod
    def create(server, ssh):

        if server.server_type == ServerType.LINUX:
            return LinuxCollector(ssh)

        raise ValueError(f"Unsupported server type: {server.server_type}")
