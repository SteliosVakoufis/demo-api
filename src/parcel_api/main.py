from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from parcel_api.api.parcels import router as parcels_router
from parcel_api.database import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(title="Parcel API", version="0.2.0", lifespan=lifespan)
app.include_router(parcels_router)

