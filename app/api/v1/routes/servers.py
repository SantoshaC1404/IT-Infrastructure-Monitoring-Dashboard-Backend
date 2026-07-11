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
