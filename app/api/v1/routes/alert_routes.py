from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.alert.alert import AlertResponse

from app.services.alert.alert_service import AlertService

from app.services.alert.alert_mapper import alert_to_response

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


# LATEST ALERTS


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_alerts(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):

    alerts = AlertService(db).get_latest(limit)

    return [alert_to_response(alert) for alert in alerts]


# OPEN ALERTS


@router.get(
    "/open",
    response_model=list[AlertResponse],
)
def get_open_alerts(
    db: Session = Depends(get_db),
):

    alerts = AlertService(db).get_open_alerts()

    return [alert_to_response(alert) for alert in alerts]


# ACKNOWLEDGE


@router.post(
    "/{alert_id}/acknowledge",
    response_model=AlertResponse,
)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):

    alert = AlertService(db).acknowledge(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    db.commit()

    return alert_to_response(alert)


# RESOLVE


@router.post(
    "/{alert_id}/resolve",
    response_model=AlertResponse,
)
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):

    alert = AlertService(db).resolve(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    db.commit()

    return alert_to_response(alert)
