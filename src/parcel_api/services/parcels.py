from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from parcel_api.models import Parcel
from parcel_api.repositories.parcels import ParcelRepository
from parcel_api.schemas import ParcelCreate


class ParcelNotFoundError(Exception):
    pass


class ParcelService:
    def __init__(self, session: AsyncSession, repository: ParcelRepository) -> None:
        self._session = session
        self._repository = repository

    async def create(self, payload: ParcelCreate) -> Parcel:
        async with self._session.begin():
            parcel = await self._repository.add(Parcel(**payload.model_dump()))
        await self._session.refresh(parcel)
        return parcel

    async def get(self, parcel_id: UUID) -> Parcel:
        parcel = await self._repository.get(parcel_id)
        if parcel is None:
            raise ParcelNotFoundError
        return parcel

    async def list(self, owner_tax_number: str | None, limit: int) -> list[Parcel]:
        return await self._repository.list(owner_tax_number, limit)

