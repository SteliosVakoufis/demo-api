from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ParcelCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    owner_tax_number: str = Field(min_length=9, max_length=16)
    area: float = Field(gt=0)


class ParcelRead(ParcelCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

