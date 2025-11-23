from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum # Luettelo
from typing import Optional


class SensorState(str, Enum):
    NORMAL = "normal"
    ERROR = "error"

class BlockBase(SQLModel):
    name: str = Field(index=True, unique=True) #Ei kahta samaa lohkoa.

#Tietokantataulu
class Block(BlockBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensors: list["Sensor"] = Relationship(back_populates="block")


class BlockOut(BlockBase):
    id: int

#Anturin yksiköinti
class SensorBase(SQLModel):
    identifier: str = Field(index=True, unique=True)
    block_id: int = Field(foreign_key="block.id")
    current_state: SensorState = Field(default=SensorState.NORMAL)


class SensorIn(SQLModel):
    identifier: str
    block_id: int

#Linkkaukset muutoksiin, sekä deletessä poisto kaikki mittaukset ja muutokset.
class Sensor(SensorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    block: Block = Relationship(back_populates="sensors")
    measurements: list["Measurement"] = Relationship(back_populates="sensor", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    state_changes: list["StateChange"] = Relationship(back_populates="sensor", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class SensorOut(SQLModel):
    id: int
    identifier: str
    block_id: int
    current_state: SensorState

#Lohkon nimi ja viimeisin mittaus
class SensorDetailOut(SensorOut):
    block_name: str
    latest_measurement: Optional[float] = None
    latest_measurement_timestamp: Optional[datetime] = None


class MeasurementBase(SQLModel):
    temperature: float = Field(description="Temperature in Celsius with one decimal precision")
    timestamp: datetime = Field(default_factory=datetime)


class MeasurementIn(MeasurementBase):
    sensor_identifier: str

#Mittauksen linkitys oikeaan anturiin (id)
class Measurement(MeasurementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    sensor: Sensor = Relationship(back_populates="measurements")


class MeasurementOut(MeasurementBase):
    id: int
    sensor_id: int

#Lokitus
class StateChangeBase(SQLModel):
    old_state: SensorState
    new_state: SensorState
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StateChangeIn(SQLModel):
    sensor_identifier: str
    new_state: SensorState

#Tietokantataulun linkitys anturiin
class StateChange(StateChangeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    sensor: Sensor = Relationship(back_populates="state_changes")


class StateChangeOut(StateChangeBase):
    id: int
    sensor_id: int


class SensorStateUpdateRequest(SQLModel):
    new_state: SensorState


class SensorBlockUpdateRequest(SQLModel):
    new_block_id: int
