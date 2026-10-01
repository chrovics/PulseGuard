from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Creăm engine-ul asincron
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Setează pe True dacă vrei să vezi query-urile SQL printate în terminal
    future=True
)

# Creăm fabrica de sesiuni
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Baza pentru modelele noastre (ORM)
Base = declarative_base()

# Dependență pentru a injecta sesiunea în rutele FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
