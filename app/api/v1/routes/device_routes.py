from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate,
)
from app.schemas.test_connection import TestConnectionRequest, TestConnectionResponse
from app.services.device.device_service import DeviceService
from app.services.device.test_connection_service import TestConnectionService

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


@router.post(
    "",
    response_model=DeviceResponse,
)
def create_device(
    request: DeviceCreate,
    db: Session = Depends(get_db),
):
    return DeviceService(db).create_device(request)


@router.get(
    "",
    response_model=list[DeviceResponse],
)
def get_all_devices(
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_all_devices()


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device_by_id(
    device_id: int,
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_device_by_id(device_id)


@router.get(
    "/ip/{ip_address}",
    response_model=DeviceResponse,
)
def get_device_by_ip(
    ip_address: str,
    db: Session = Depends(get_db),
):
    return DeviceService(db).get_device_by_ip(ip_address)


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


@router.post(
    "/test-connection",
    response_model=TestConnectionResponse,
)
def test_connection(
    request: TestConnectionRequest,
):
    return TestConnectionService().test(request)
