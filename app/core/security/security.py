import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(subject: str) -> tuple[str, str, datetime]:
    """
    Creates a signed JWT.

    Returns (token, jti, expires_at) - the caller gets the raw token to
    hand back to the client, plus the jti/expiry needed elsewhere
    (e.g. to revoke this exact token on logout).
    """

    jti = str(uuid.uuid4())

    issued_at = datetime.now(timezone.utc)

    expires_at = issued_at + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": subject,
        "jti": jti,
        "iat": issued_at,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token, jti, expires_at


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        return None
