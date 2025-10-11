from pydantic import BaseModel, ConfigDict, Field, field_serializer
import datetime
from datetime import time

class SAppointments(BaseModel):
    doctor_id: int | None = Field(None, description="ID of the doctor")
    services_id: int | None = Field(None, description="ID of the service")
    date: str = Field(..., description="Date of the appointment in YYYY-MM-DD format", examples=["2023-10-15"])
    start_time: str | None = Field(None, description="Start time of the appointment in HH:MM format", examples=["14:30"])
    end_time: str | None = Field(None, description="End time of the appointment in HH:MM format", examples=["15:30"])
    

    model_config = ConfigDict(from_attributes=True)

class SAppointmentsInDB(BaseModel):
    id: int
    doctor_id: int | None = Field(None, description="ID of the doctor")
    services_id: int | None = Field(None, description="ID of the service")
    date: datetime.date = Field(..., description="Date of the appointment in YYYY-MM-DD format", examples=["2023-10-15"])
    start_time: time | None = Field(None, description="Start time of the appointment in HH:MM format", examples=["14:30"])
    end_time: time | None = Field(None, description="End time of the appointment in HH:MM format", examples=["15:30"])
    user_id: int | None = None
    status: str = Field(..., examples=["booked"]) # e.g., "booked", "cancelled"
    
    @field_serializer("date")
    def serialize_date(self, date_value: datetime.date, _info):
        if isinstance(date_value, str):
            return date_value
        return date_value.isoformat() if date_value else None

    @field_serializer("start_time", "end_time")
    def serialize_time(self, time_value: time, _info):
        if isinstance(time_value, str):
            return time_value
        return time_value.strftime("%H:%M:%S") if time_value else None

    model_config = ConfigDict(from_attributes=True)