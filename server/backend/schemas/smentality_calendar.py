from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Dict, List, Optional, Any


class SMentalityMonthData(BaseModel):
    mood: Optional[List[int]] = Field(default_factory=list)
    anxiety: Optional[List[int]] = Field(default_factory=list)
    confidence: Optional[List[int]] = Field(default_factory=list)

    @field_validator("*", mode="before")
    @classmethod
    def ensure_list_of_ints(cls, v):
        if v is None:
            return []
        if not isinstance(v, list):
            raise ValueError("Каждое поле должно быть списком чисел.")
        for item in v:
            if not isinstance(item, int):
                raise ValueError("Все элементы должны быть числами.")
        return v


class SMentalityCalendar(BaseModel):
    mentality: Dict[
        str,  # Год, например "2025"
        List[Dict[str, SMentalityMonthData]],  # Месяц, например "01"
    ]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("mentality", mode="before")
    @classmethod
    def validate_mentality_structure(cls, values: dict):
        mentality = values
        if not isinstance(mentality, dict):
            raise ValueError("Поле 'mentality' должно быть объектом (dict).")

        for year, months_list in mentality.items():
            if not isinstance(year, str) or not year.isdigit():
                raise ValueError(
                    f"Ключ '{year}' должен быть строкой-годом, например '2025'."
                )
            if not isinstance(months_list, list):
                raise ValueError(f"Значение для года '{year}' должно быть списком.")
            for entry in months_list:
                if not isinstance(entry, dict):
                    raise ValueError(
                        f"Каждый элемент в году '{year}' должен быть объектом с месяцом."
                    )
                for month, data in entry.items():
                    if not isinstance(month, str) or not month.isdigit():
                        raise ValueError(f"Месяц '{month}' должен быть строкой-числом.")
                    if len(month) == 1:
                        # Автоматическая нормализация — превращаем "1" → "01"
                        normalized_month = month.zfill(2)
                        entry[normalized_month] = data
                        del entry[month]
                    elif len(month) != 2:
                        raise ValueError(
                            f"Некорректный формат месяца '{month}' (нужно '01'-'12')."
                        )

        return values


class SMentalityCalendarOut(SMentalityCalendar):
    id: int
    user_id: int = Field(examples=1)

    model_config = ConfigDict(from_attributes=True)
