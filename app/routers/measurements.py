from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from ..database.database import get_session
from ..database import measurements_crud
from ..database.models import MeasurementIn, MeasurementOut, StateChangeIn

router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.post("", response_model=MeasurementOut, status_code=status.HTTP_201_CREATED)
def receive_measurement(
    *,
    session: Session = Depends(get_session),
    measurement_in: MeasurementIn
):
    """Vastaanota lämpötilamittaus anturilta"""
    return measurements_crud.create_measurement(session, measurement_in)


@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement(
    *,
    session: Session = Depends(get_session),
    measurement_id: int
):
    """Poista mittaus id:llä"""
    measurements_crud.delete_measurement(session, measurement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/state-changes", status_code=status.HTTP_200_OK)
def receive_state_change(
    *,
    session: Session = Depends(get_session),
    state_change_in: StateChangeIn
):
    """VAstaanota anturin tilamuutos"""
    return measurements_crud.record_sensor_state_change(
        session, 
        state_change_in.sensor_identifier, 
        state_change_in.new_state
    )
