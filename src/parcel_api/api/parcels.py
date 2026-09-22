from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from parcel_api.database import get_session
from parcel_api.repositories.parcels import ParcelRepository
from parcel_api.schemas import ParcelCreate, ParcelRead
from parcel_api.services.parcels import ParcelNotFoundError, ParcelService

router = APIRouter(prefix="/parcels", tags=["parcels"])
Session = Annotated[AsyncSession, Depends(get_session)]


def service_for(session: AsyncSession) -> ParcelService:
    return ParcelService(session, ParcelRepository(session))


@router.post("", response_model=ParcelRead, status_code=201)
async def create_parcel(payload: ParcelCreate, session: Session) -> ParcelRead:
    parcel = await service_for(session).create(payload)
    return ParcelRead.model_validate(parcel)


@router.get("/{parcel_id}", response_model=ParcelRead)
async def get_parcel(parcel_id: UUID, session: Session) -> ParcelRead:
    try:
        parcel = await service_for(session).get(parcel_id)
    except ParcelNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Parcel not found") from exc
    return ParcelRead.model_validate(parcel)


@router.get("", response_model=list[ParcelRead])
async def list_parcels(
    session: Session,
    owner_tax_number: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[ParcelRead]:
    parcels = await service_for(session).list(owner_tax_number, limit)
    return [ParcelRead.model_validate(parcel) for parcel in parcels]

