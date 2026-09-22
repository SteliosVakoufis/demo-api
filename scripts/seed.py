import asyncio

from sqlalchemy import select

from parcel_api.database import session_factory
from parcel_api.models import Parcel


async def main() -> None:
    async with session_factory() as session, session.begin():
        existing = await session.scalar(select(Parcel.id).limit(1))
        if existing is not None:
            print("Seed data already exists")
            return
        session.add_all(
            [
                Parcel(code="P-1001", owner_tax_number="123456789", area=12.4),
                Parcel(code="P-1002", owner_tax_number="987654321", area=7.8),
            ]
        )
    print("Seeded two parcels")


if __name__ == "__main__":
    asyncio.run(main())

