from app.monitoring.collectors.metrics_collector_service import (
    MetricsCollectorService,
)
from app.monitoring.parsers.linux_metrics_parser import (
    LinuxMetricsParser,
)


class LinuxMetricsCollector(MetricsCollectorService):

    def __init__(
        self,
        connector,
        commands,
    ):
        super().__init__(
            connector,
            commands,
            LinuxMetricsParser(),
        )
