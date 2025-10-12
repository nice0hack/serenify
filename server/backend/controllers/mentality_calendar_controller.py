from unittest import result
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from controllers.base_controller import BaseController
from models import MentalityCalendarModel
from schemas import SMentalityCalendar, SUserTokenPayload, SMentalityCalendarOut
from sqlalchemy.ext.asyncio import AsyncSession


class MentalityCalendarController(
    BaseController[MentalityCalendarModel, SMentalityCalendar]
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MentalityCalendarModel, SMentalityCalendar)

    async def get_by_user(self, user: SUserTokenPayload):
        user_id = user.id
        stmt = select(MentalityCalendarModel).where(MentalityCalendarModel.user_id == user_id)
        result = await self.session.execute(stmt)
        calendar = result.scalar_one_or_none()

        return SMentalityCalendarOut.model_validate(calendar)
    
    async def create_and_update_calendar(
    self,
    user: SUserTokenPayload,
    calendar: SMentalityCalendar
):
        user_id = user.id

        stmt = select(MentalityCalendarModel).where(MentalityCalendarModel.user_id == user_id)
        result = await self.session.execute(stmt)
        exists_calendar = result.scalar_one_or_none()

        new_data = calendar.model_dump().get("mentality", {})

        if exists_calendar is None:
            calendar_model = MentalityCalendarModel(
                user_id=user_id,
                mentality=new_data
            )
            self.session.add(calendar_model)
            await self.session.commit()
            return {"success": True, "msg":"Данные созданы"}
        else:
            current_data = exists_calendar.mentality or {}

            # Глубокое слияние по годам и месяцам
            for year, new_entries in new_data.items():
                if year not in current_data:
                    # Новый год — добавляем целиком
                    current_data[year] = new_entries
                    continue

                # Иначе — идём по каждому месяцу внутри года
                for year, new_entries in new_data.items():
                    if year not in current_data:
                        current_data[year] = new_entries
                    else:
                        for new_entry in new_entries:
                            for month, new_values in new_entry.items():
                                # Ищем, есть ли этот месяц
                                month_entry = next((m for m in current_data[year] if month in m), None)
                                if month_entry:
                                    existing_month = month_entry[month]
                                    for key, val in new_values.items():
                                        if key in existing_month:
                                            # 🔧 сохраняем дубликаты, порядок
                                            if isinstance(existing_month[key], list) and isinstance(val, list):
                                                existing_month[key].extend(val)
                                            else:
                                                existing_month[key] = val
                                        else:
                                            existing_month[key] = val
                                else:
                                    current_data[year].append({month: new_values})
            print(current_data)
            exists_calendar.mentality = current_data
            flag_modified(exists_calendar, "mentality")

            await self.session.commit()
            await self.session.refresh(exists_calendar)
            return {"success": True, "msg":"Обновлены данные"}

        

