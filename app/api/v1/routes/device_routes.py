from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.device.device import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate,
)
from app.schemas.monitoring.monitoring_snapshot import DeviceHistoryResponse
from app.schemas.test.test_connection import (
    TestConnectionRequest,
    TestConnectionResponse,
)
from app.services.device.device_service import DeviceService
from app.services.device.test_connection_service import TestConnectionService

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


# CREATE DEVICE
@router.post(
    "",
    response_model=DeviceResponse,
)
def create_device(
    request: DeviceCreate,
    db: Session = Depends(get_db),
):
    return DeviceService(db).create_device(request)


# GET ALL DEVICES
@router.get(
    "",
    response_model=list[DeviceResponse],
)
def get_all_devices(
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_all_devices()


# CRITICAL DEVICES
@router.get(
    "/critical-devices",
    response_model=list[DeviceResponse],
)
def get_critical_devices(
    db: Session = Depends(get_db),
):
    return DeviceService(db).critical_devices()


# GET DEVICE BY IP
@router.get(
    "/ip/{ip_address}",
    response_model=DeviceResponse,
)
def get_device_by_ip(
    ip_address: str,
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_device_by_ip(ip_address)


# DELETE DEVICE BY IP
@router.delete(
    "/ip/{ip_address}",
)
def delete_device_by_ip(
    ip_address: str,
    db: Session = Depends(get_db),
):
    DeviceService(db).delete_device_by_ip(ip_address)

    return {
        "message": "Device deleted successfully",
    }


# TEST DEVICE CONNECTION
@router.post(
    "/test-connection",
    response_model=TestConnectionResponse,
)
def test_connection(
    request: TestConnectionRequest,
):
    return TestConnectionService().test(request)


# DEVICE HISTORY
@router.get(
    "/{device_id}/history",
    response_model=list[DeviceHistoryResponse],
)
def get_device_history(
    device_id: int,
    hours: int | None = Query(default=None, ge=1),
    days: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_device_history(device_id, hours=hours, days=days)


# UPDATE DEVICE - PATCH
@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_device(
    device_id: int,
    request: DeviceUpdate,
    db: Session = Depends(get_db),
):
    return DeviceService(db).update_device(device_id, request)


# UPDATE DEVICE - PUT
@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_device_put(
    device_id: int,
    request: DeviceUpdate,
    db: Session = Depends(get_db),
):
    return DeviceService(db).update_device(device_id, request)


# DELETE DEVICE BY ID
@router.delete(
    "/{device_id}",
)
def delete_device_by_id(
    device_id: int,
    db: Session = Depends(get_db),
):
    DeviceService(db).delete_device_by_id(device_id)

    return {
        "message": "Device deleted successfully",
    }


# GET DEVICE BY ID
@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device_by_id(
    device_id: int,
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_device_by_id(device_id)
