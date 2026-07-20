from app.monitoring.collectors.metrics_collector_service import (
    MetricsCollectorService,
)

from app.monitoring.parsers.windows_metrics_parser import (
    WindowsMetricsParser,
)


class WindowsMetricsCollector(MetricsCollectorService):

    def __init__(self, connector, commands):
        super().__init__(
            connector,
            commands,
            WindowsMetricsParser(),
        )
