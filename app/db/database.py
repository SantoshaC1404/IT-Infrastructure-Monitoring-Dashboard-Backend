from sqlalchemy import create_engine
from app.core.config import settings

# engine = create_engine(
#     settings.DATABASE_URL.replace("%", "%%"), pool_pre_ping=True, echo=settings.DEBUG
# )
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)

print("Database URL:", settings.DATABASE_URL)
