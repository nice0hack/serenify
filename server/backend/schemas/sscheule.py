from pydantic import BaseModel, Field, ConfigDict


class SScheduleEntry(BaseModel):
    weekday: int = Field(..., description="Day of the week (0=Monday, 6=Sunday)", example=0)
    start_time: str = Field(..., description="Start time in HH:MM:SS format", example="09:00:00")
    end_time: str = Field(..., description="End time in HH:MM:SS format", example="17:00:00")
    slot_duration: int = Field(30, description="Duration of each slot in minutes", example=30)

    model_config = ConfigDict(from_attributes=True)

class SExceptionEntry(BaseModel):
    date: str = Field(..., description="Date of the exception in YYYY-MM-DD format", example="2023-10-31")
    is_day_off: bool = Field(False, description="Is it a day off?", example=False)
    start_time: str | None = Field(None, description="Start time in HH:MM:SS format (if not a day off)", example="10:00:00")
    end_time: str | None = Field(None, description="End time in HH:MM:SS format (if not a day off)", example="15:00:00")

    model_config = ConfigDict(from_attributes=True)
