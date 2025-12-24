from decimal import Decimal
from uuid import uuid4

# با نوشتن عبارت type: ignore دیگر playcene کاری به ارور های این قسمت ندارد
import jdatetime  # type: ignore
from pydantic import BaseModel, Field, field_validator


class LabResult(BaseModel):
    sampleID: str = Field(default_factory=lambda: str(uuid4()))
    year: str = Field(..., min_length=4, max_length=4)
    month: str = Field(..., min_length=2, max_length=2)
    day: str = Field(..., min_length=2, max_length=2)
    time: str = Field(..., min_length=4, max_length=5)
    timestamp: int | None = None
    klin: int
    above40: Decimal
    carbondioxide: Decimal
    par05: Decimal
    par51: Decimal
    par10: Decimal
    par16: Decimal
    par60: Decimal

    @field_validator("year", mode="before")
    def check_year(cls, v):
        if not v.isdigit():
            raise ValueError("Year must be numeric")
        year_int = int(v)
        if not (1400 <= year_int):
            raise ValueError("Year must be between 1400 and above")
        return v

    @field_validator("month", mode="before")
    def check_month_range(cls, v):
        if not v.isdigit():
            raise ValueError("Month must be numeric")
        month_int = int(v)
        if not (1 <= month_int <= 12):
            raise ValueError("Month must be between 01 and 12")
        return v

    @field_validator("day", mode="before")
    def check_day_range(cls, v):
        if not v.isdigit():
            raise ValueError("Day must be numeric")
        day_int = int(v)
        if not (1 <= day_int <= 31):
            raise ValueError("Day must be between 01 and 31")
        return v

    def model_post_init(self, __context):
        """بعد از ساخت مدل، timestamp را محاسبه کن"""
        self.timestamp = int(
            jdatetime.datetime(
                year=int(self.year),
                month=int(self.month),
                day=int(self.day),
                hour=int(self.time[:2]),
                minute=int(self.time[2:]),
            )
            .togregorian()
            .timestamp()
        )


# result = LabResult(
#     year="1402",
#     month="12",
#     day="24",
#     time="1330",
#     klin=1,
#     above40=Decimal("12.5"),
#     carbondioxide=Decimal("3.2"),
#     par05=Decimal("0.5"),
#     par51=Decimal("1.1"),
#     par10=Decimal("2.0"),
#     par16=Decimal("1.6"),
#     par60=Decimal("6.0"),
# )
# print(result)


# result = sampleID='8ec8ec4c-b1e4-4596-a04c-d0b0a1bd198d'
#             year='1402'
#             month='12'
#             day='24'
#             time='1330'
#             timestamp=1710410400
#             klin=1
#             above40=Decimal('12.5')
#             carbondioxide=Decimal('3.2')
#             par05=Decimal('0.5')
#             par51=Decimal('1.1')
#             par10=Decimal('2.0')
#             par16=Decimal('1.6')
#             par60=Decimal('6.0')
