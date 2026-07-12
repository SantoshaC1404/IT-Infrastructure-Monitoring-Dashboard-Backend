from app.services.ssh_service import SSHService
from app.collectors.factory import CollectorFactory


def collect(self, server):

    ssh = SSHService(server)

    collector = CollectorFactory.create(server, ssh)

    metrics = collector.collect()

    self.repository.save_snapshot(server, metrics)

    return metrics
