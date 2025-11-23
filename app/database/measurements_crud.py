from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import Measurement, MeasurementIn, StateChange, StateChangeIn, SensorState

# Aikaleimat
from .sensors_crud import get_sensor_by_identifier
from datetime import datetime


# Mittauksen tallennus tietokantaan.
def create_measurement(session: Session, measurement_in: MeasurementIn):
    """Luo uusi lämpötilamittaus anturilta"""
    sensor = get_sensor_by_identifier(session, measurement_in.sensor_identifier)

#Virhetila    
    if sensor.current_state == SensorState.ERROR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Anturi {sensor.identifier} virhetilassa, eikä voi lähettää mittauksia"
        )
# Lämpötilan yhdellä desimaalilla pyöristys
    temperature = round(measurement_in.temperature, 1)

 # Luo uuden tietokantarivin   
    measurement = Measurement(
        sensor_id=sensor.id,
        temperature=temperature,
        timestamp=measurement_in.timestamp
    )
    
    session.add(measurement)
    session.commit()
    session.refresh(measurement)
    
    return measurement

#Poista mittaus -prosessi
def delete_measurement(session: Session, measurement_id: int):
    """Poista mittaus"""
    measurement = session.get(Measurement, measurement_id)
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mittausta {measurement_id} ei löytynyt."
        )
    
    session.delete(measurement)
    session.commit()

#Tilamuutoksen päivittäminen
def record_sensor_state_change(session: Session, sensor_identifier: str, new_state: SensorState):
    """Kirjaa anturin tilamuutos"""
    sensor = get_sensor_by_identifier(session, sensor_identifier)
    
    old_state = sensor.current_state

    #Jos vanha ja uusi tila sama, niin ei tehdä mitään.
    if old_state == new_state:
        return {
            "message": f"Anturi {sensor_identifier} on tilassa {new_state}.",
            "sensor_id": sensor.id,
            "current_state": sensor.current_state
        }
    
    state_change = StateChange(
        sensor_id=sensor.id,
        old_state=old_state,
        new_state=new_state,
        timestamp=datetime.utcnow()
    )
    session.add(state_change)
    
    sensor.current_state = new_state
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    
    # tilamuutoksen palautus
    return {
        "message": f"Anturin {sensor_identifier} tilamuutos on kirjattu.",
        "sensor_id": sensor.id,
        "old_state": old_state,
        "new_state": new_state,
        "timestamp": state_change.timestamp
    }
