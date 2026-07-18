from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
)
from app.services.device.device_service import ServerService

router = APIRouter(
    prefix="/servers",
    tags=["servers"],
)


@router.post(
    "",
    response_model=ServerResponse,
)
def create_server(
    request: ServerCreate,
    db: Session = Depends(get_db),
):
    return ServerService(db).create_server(request)


@router.get(
    "",
    response_model=list[ServerResponse],
)
def get_all_servers(
    db: Session = Depends(get_db),
):
    return ServerService(db).get_all_servers()


@router.get(
    "/{server_id}",
    response_model=ServerResponse,
)
def get_server_by_id(
    server_id: int,
    db: Session = Depends(get_db),
):
    return ServerService(db).get_server_by_id(server_id)


@router.get(
    "/ip/{ip_address}",
    response_model=ServerResponse,
)
def get_server_by_ip(
    ip_address: str,
    db: Session = Depends(get_db),
):
    return ServerService(db).get_server_by_ip(ip_address)


@router.delete(
    "/{server_id}",
)
def delete_server_by_id(
    server_id: int,
    db: Session = Depends(get_db),
):
    ServerService(db).delete_server_by_id(server_id)

    return {
        "message": "Server deleted successfully",
    }


@router.delete(
    "/{ip_address}",
)
def delete_server_by_ip(
    ip_address: str,
    db: Session = Depends(get_db),
):
    ServerService(db).delete_server_by_ip(ip_address)

    return {
        "message": "Server deleted successfully",
    }
