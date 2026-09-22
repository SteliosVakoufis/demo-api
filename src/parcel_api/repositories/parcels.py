from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from parcel_api.models import Parcel


class ParcelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, parcel: Parcel) -> Parcel:
        self._session.add(parcel)
        await self._session.flush()
        return parcel

    async def get(self, parcel_id: UUID) -> Parcel | None:
        return await self._session.get(Parcel, parcel_id)

    async def list(self, owner_tax_number: str | None, limit: int) -> list[Parcel]:
        statement: Select[tuple[Parcel]] = select(Parcel).order_by(Parcel.code).limit(limit)
        if owner_tax_number is not None:
            statement = statement.where(Parcel.owner_tax_number == owner_tax_number)
        return list((await self._session.scalars(statement)).all())

