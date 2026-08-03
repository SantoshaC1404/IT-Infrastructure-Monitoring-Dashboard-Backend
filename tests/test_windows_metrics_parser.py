from app.monitoring.parsers.windows_metric_parser import WindowsMetricsParser


def test_last_login_returns_none_for_blank_output():
    parser = WindowsMetricsParser()

    assert parser.last_login("   \n\t") is None
