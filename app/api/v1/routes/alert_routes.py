from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.device_alert import Alert
from app.schemas.alert.alert import AlertResponse
from app.services.alert.alert_service import AlertService

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


def serialize_alert(alert: Alert):

    return AlertResponse(
        id=alert.id,
        device_id=alert.device_id,
        device_name=alert.device.name,
        device_ip=alert.device.ip_address,
        severity=alert.severity,
        title=alert.title,
        message=alert.message,
        metric=alert.metric,
        current_value=alert.metric_value,
        threshold=alert.threshold,
        status=alert.status,
        created_at=alert.created_at,
        acknowledged_at=alert.acknowledged_at,
        resolved_at=alert.resolved_at,
    )


# ---------------------------------------------------------
# LATEST ALERTS
# ---------------------------------------------------------


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_alerts(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
):

    alerts = AlertService(db).get_latest(limit)

    return [serialize_alert(alert) for alert in alerts]


# ---------------------------------------------------------
# OPEN ALERTS
# ---------------------------------------------------------


@router.get(
    "/open",
    response_model=list[AlertResponse],
)
def get_open_alerts(
    db: Session = Depends(get_db),
):

    alerts = AlertService(db).get_open_alerts()

    return [serialize_alert(alert) for alert in alerts]


# ---------------------------------------------------------
# ACKNOWLEDGE
# ---------------------------------------------------------


@router.post(
    "/{alert_id}/acknowledge",
    response_model=AlertResponse,
)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):

    service = AlertService(db)

    alert = service.acknowledge(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    db.commit()

    return serialize_alert(alert)


# ---------------------------------------------------------
# RESOLVE
# ---------------------------------------------------------


@router.post(
    "/{alert_id}/resolve",
    response_model=AlertResponse,
)
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):

    service = AlertService(db)

    alert = service.resolve(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    db.commit()

    return serialize_alert(alert)
