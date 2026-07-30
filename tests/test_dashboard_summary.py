from types import SimpleNamespace

from app.repositories.dashboard_repository import DashboardRepository


class DummyResult:
    def __init__(self):
        self.total_devices = 5
        self.online_devices = 3
        self.offline_devices = 2
        self.monitoring_enabled = 4
        self.monitoring_disabled = 1
        self.linux_devices = 2
        self.windows_devices = 1
        self.network_devices = 2


class DummySession:
    def query(self, *args, **kwargs):
        return self

    def one(self):
        return DummyResult()


def test_dashboard_repository_get_summary_maps_expected_fields():
    repository = DashboardRepository(db=DummySession())
    summary = repository.get_summary()

    assert summary.total_devices == 5
    assert summary.online_devices == 3
    assert summary.offline_devices == 2
    assert summary.monitoring_enabled == 4
    assert summary.monitoring_disabled == 1
    assert summary.device_types == {"LINUX": 2, "WINDOWS": 1, "NETWORK": 2}
