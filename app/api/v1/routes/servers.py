from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.server import (
    ServerCreate,
    ServerResponse,
)
from app.services.server_service import ServerService
from app.api.deps import get_db

router = APIRouter(
    prefix="/servers",
    tags=["servers"],
)


@router.post(
    "",
    response_model=ServerResponse,
)
def create_server(
    create_request: ServerCreate,
    db: Session = Depends(get_db),
):
    server_service = ServerService(db=db)

    try:
        return server_service.create_server(create_request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[ServerResponse],
)
def get_all_servers(db: Session = Depends(get_db)):
    return ServerService(db).get_all_servers()


@router.get(
    "/{server_id}",
    response_model=ServerResponse,
)
def get_server_by_id(server_id: int, db: Session = Depends(get_db)):
    server_service = ServerService(db)

    server = server_service.server_repository.get_by_id(server_id)

    if server is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )

    return server


@router.delete(
    "/{server_id}",
    response_model=ServerResponse,
)
def delete_server_bby_id(server_id: int, db: Session = Depends(get_db)):
    server_service = ServerService(db)

    server = server_service.server_repository.get_by_id(server_id)

    if server is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )

    server_service.server_repository.delete(server_id)

    return {"message": "Server deleted successfully"}
