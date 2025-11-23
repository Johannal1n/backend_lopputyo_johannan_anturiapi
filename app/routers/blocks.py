from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from ..database.database import get_session
from ..database import blocks_crud, sensors_crud
from ..database.models import BlockOut, BlockBase, SensorDetailOut

router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.get("", response_model=list[BlockOut])
def get_blocks(
    *,
    session: Session = Depends(get_session)
):
    """Hae kaikki lohkot"""
    return blocks_crud.get_all_blocks(session)


@router.post("", response_model=BlockOut, status_code=status.HTTP_201_CREATED)
def create_block(
    *,
    session: Session = Depends(get_session),
    block_in: BlockBase
):
    """Luo uusi lohko"""
    return blocks_crud.create_block(session, block_in.name)


@router.get("/{block_id}", response_model=BlockOut)
def get_block(
    *,
    session: Session = Depends(get_session),
    block_id: int
):
    """Hae lohko id:llä"""
    return blocks_crud.get_block_by_id(session, block_id)


@router.get("/{block_id}/sensors", response_model=list[SensorDetailOut])
def get_block_sensors(
    *,
    session: Session = Depends(get_session),
    block_id: int
):
    """Hae lohkon anturit"""
    return sensors_crud.get_sensors_by_block(session, block_id)
