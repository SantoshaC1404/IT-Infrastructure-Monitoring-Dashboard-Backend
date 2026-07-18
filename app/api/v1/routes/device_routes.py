from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
)
from app.services.device.device_service import DeviceService

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
    "/{ip_address}",
)
def delete_device_by_ip(
    ip_address: str,
    db: Session = Depends(get_db),
):
    DeviceService(db).delete_device_by_ip(ip_address)

    return {
        "message": "Device deleted successfully",
    }
