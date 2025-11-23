from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import (
    Sensor, SensorIn, SensorDetailOut, SensorState,
    Block, StateChange, Measurement
)
from datetime import datetime


def get_all_sensors(session: Session):
    """Hae kaikki anturit"""
    sensors = session.exec(select(Sensor)).all()
    return sensors


def get_sensors_by_state(session: Session, state: SensorState):
    """Hae anturit tilan perusteella"""
    sensors = session.exec(select(Sensor).where(Sensor.current_state == state)).all()
    return sensors


def create_sensor(session: Session, sensor_in: SensorIn):
    """Luo uusi anturi"""
    block = session.get(Block, sensor_in.block_id)
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lohkoa id:llä {sensor_in.block_id} ei löytynyt."
        )
    
    existing = session.exec(select(Sensor).where(Sensor.identifier == sensor_in.identifier)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Anturi tunnisteella {sensor_in.identifier} on jo olemassa."
        )
    
    sensor = Sensor.model_validate(sensor_in)
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor


def get_sensor_by_id(session: Session, sensor_id: int):
    """Hae anturi id:llä"""
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anturia id:llä {sensor_id} ei löytynyt."
        )
    return sensor


def get_sensor_by_identifier(session: Session, identifier: str):
    """Hae anturi tunnisteen avulla"""
    sensor = session.exec(select(Sensor).where(Sensor.identifier == identifier)).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anturi tunnisteella {identifier} ei löydy"
        )
    return sensor


def update_sensor_state(session: Session, sensor_id: int, new_state: SensorState):
    """Päivitä anturin tilamuutos"""
    sensor = get_sensor_by_id(session, sensor_id)
    old_state = sensor.current_state
    
    if old_state == new_state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Anturi on jo tilassa {new_state} "
        )
    #Historiaa varten tallennetaan vanha tila ja uusi tila erilliseen tauluun
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
    
    return sensor


def update_sensor_block(session: Session, sensor_id: int, new_block_id: int):
    """Päivitä mihin lohkoon anturi kuuluu"""
    sensor = get_sensor_by_id(session, sensor_id)

    block = session.get(Block, new_block_id)
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lohkoa id:llä {new_block_id} ei löydy."
        )
    
    sensor.block_id = new_block_id
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    
    return sensor


def get_sensors_by_block(session: Session, block_id: int):
    """Hae lohkon kaikki anturit ja niiden viimeisin mittaus"""
    block = session.get(Block, block_id)
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lohkoa id:llä {block_id} ei löydy"
        )
    
    sensors = session.exec(select(Sensor).where(Sensor.block_id == block_id)).all()
    
    result = []
    for sensor in sensors:
        latest_measurement = session.exec(
            select(Measurement)
            .where(Measurement.sensor_id == sensor.id)
            .order_by(Measurement.timestamp.desc())
            .limit(1)
        ).first()
        
        #Yhdistetty dataobjekti
        sensor_detail = SensorDetailOut(
            id=sensor.id,
            identifier=sensor.identifier,
            block_id=sensor.block_id,
            current_state=sensor.current_state,
            block_name=block.name,
            latest_measurement=latest_measurement.temperature if latest_measurement else None,
            latest_measurement_timestamp=latest_measurement.timestamp if latest_measurement else None
        )
        result.append(sensor_detail)
    
    return result


def get_sensor_measurements(
    session: Session, 
    sensor_id: int, 
    limit: int = 10,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """Hae anturin mittaukset valinnaisella aikarajauksella"""
    sensor = get_sensor_by_id(session, sensor_id)
    
    query = select(Measurement).where(Measurement.sensor_id == sensor_id)
    
    #Ehdot alkuajan ja loppuajan perusteella
    if start_time:
        query = query.where(Measurement.timestamp >= start_time)
    if end_time:
        query = query.where(Measurement.timestamp <= end_time)
    
    query = query.order_by(Measurement.timestamp.desc())
    
    if not start_time and not end_time:
        query = query.limit(limit)
    
    measurements = session.exec(query).all()
    return measurements


def get_sensor_state_changes(session: Session, sensor_id: int):
    """Hae anturin tilamuutoshistoria"""
    sensor = get_sensor_by_id(session, sensor_id)
    
    state_changes = session.exec(
        select(StateChange)
        .where(StateChange.sensor_id == sensor_id)
        .order_by(StateChange.timestamp.desc())
    ).all()
    
    return state_changes