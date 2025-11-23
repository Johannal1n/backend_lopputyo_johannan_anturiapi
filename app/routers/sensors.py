from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from typing import Optional
from datetime import datetime

from ..database.database import get_session
from ..database import sensors_crud
from ..database.models import (
    SensorIn, SensorOut, SensorStateUpdateRequest, 
    SensorBlockUpdateRequest, SensorState, MeasurementOut, StateChangeOut
)

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("", response_model=list[SensorOut])
def get_sensors(
    *,
    session: Session = Depends(get_session),
    state: Optional[SensorState] = Query(None, description="Filter sensors by state")
):
    """Hae kaikki anturit, valinnainen suodatus tilan perusteella"""
    if state:
        return sensors_crud.get_sensors_by_state(session, state)
    return sensors_crud.get_all_sensors(session)


@router.post("", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(
    *,
    session: Session = Depends(get_session),
    sensor_in: SensorIn
):
    """Lisää uusi anturi"""
    return sensors_crud.create_sensor(session, sensor_in)


@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(
    *,
    session: Session = Depends(get_session),
    sensor_id: int
):
    """Hae anturi id:llä"""
    return sensors_crud.get_sensor_by_id(session, sensor_id)


@router.get("/{sensor_id}/measurements", response_model=list[MeasurementOut])
def get_sensor_measurements(
    *,
    session: Session = Depends(get_session),
    sensor_id: int,
    limit: int = Query(10, description="Palautettavien mittausten määrä (default 10)", ge=1),
    start_time: Optional[datetime] = Query(None, description="Suodata mittaukset tästä ajasta alkaen"),
    end_time: Optional[datetime] = Query(None, description="Suodata mittaukset tähän asti")
):
    """
    Hae anturin mittaukset.
    Palauttaa oletuksena 10 uusinta mittausta.
    Tuloksia voi rajata aikavälillä käyttämällä start_time- ja end_time -parametreja.
    """
    return sensors_crud.get_sensor_measurements(session, sensor_id, limit, start_time, end_time)


@router.get("/{sensor_id}/state-changes", response_model=list[StateChangeOut])
def get_sensor_state_changes(
    *,
    session: Session = Depends(get_session),
    sensor_id: int
):
    """Hae anturin tilamuutokset"""
    return sensors_crud.get_sensor_state_changes(session, sensor_id)


@router.patch("/{sensor_id}/state", response_model=SensorOut)
def update_sensor_state(
    *,
    session: Session = Depends(get_session),
    sensor_id: int,
    state_update: SensorStateUpdateRequest
):
    """Vaihda anturin tila"""
    return sensors_crud.update_sensor_state(session, sensor_id, state_update.new_state)


@router.patch("/{sensor_id}/block", response_model=SensorOut)
def update_sensor_block(
    *,
    session: Session = Depends(get_session),
    sensor_id: int,
    block_update: SensorBlockUpdateRequest
):
    """Vaihda anturin lohko"""
    return sensors_crud.update_sensor_block(session, sensor_id, block_update.new_block_id)
