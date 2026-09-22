from uuid import UUID, uuid4

from sqlalchemy import Float, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Parcel(Base):
    __tablename__ = "parcel"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    owner_tax_number: Mapped[str] = mapped_column(String(16), index=True)
    area: Mapped[float] = mapped_column(Float)

