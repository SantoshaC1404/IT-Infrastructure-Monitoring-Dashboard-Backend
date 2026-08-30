from app.models.device_alert import Alert


def alert_to_response(alert: Alert):

    return {
        "id": alert.id,
        "device_id": alert.device_id,
        "device_name": alert.device.name,
        "device_ip": alert.device.ip_address,
        "severity": alert.severity,
        "title": alert.title,
        "message": alert.message,
        "metric": alert.metric,
        "current_value": alert.metric_value,
        "threshold": alert.threshold,
        "status": alert.status,
        "created_at": alert.created_at,
        "acknowledged_at": alert.acknowledged_at,
        "resolved_at": alert.resolved_at,
    }
