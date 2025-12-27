from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

# با نوشتن عبارت type: ignore دیگر playcene کاری به ارور های این قسمت ندارد
import jdatetime  # type: ignore
from pydantic import BaseModel, Field, field_validator


class LabResult(BaseModel):
    timestamp: int | str = "NA"
    year: str = Field(..., min_length=4, max_length=4)
    month: str = Field(..., min_length=2, max_length=2)
    day: str = Field(..., min_length=2, max_length=2)
    time: str = Field(..., min_length=4, max_length=5)
    klin1: str = "Not Tested"
    klin2: str = "Not Tested"
    above40: str = "Not Tested"
    par05: str = "Not Tested"
    par51: str = "Not Tested"
    par10: str = "Not Tested"
    par16: str = "Not Tested"
    par60: str = "Not Tested"

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

    @field_validator("klin1", "klin2", "above40", mode="before")
    def safe_decimal_co2(value) -> str:
        try:
            round = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            return str(round)
        except (InvalidOperation, ValueError):
            return "Not Tested"

    @field_validator("par05", "par51", "par60", mode="before")
    def safe_decimal_par(value) -> str:
        try:
            round = Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            return str(round)
        except (InvalidOperation, ValueError):
            return "Not Tested"

    def model_post_init(self, __context):
        """بعد از ساخت مدل، فیلدهای محاسباتی را مقداردهی کن"""

        # timestamp از تاریخ شمسی ساخته می‌شود
        hour = int(self.time[:2])
        minute = int(self.time[2:])
        year_int = int(self.year)
        month_int = int(self.month)
        day_int = int(self.day)  # اگر ساعت بین 00:00 تا 07:59 بود → یک روز جلو برو
        base_date = jdatetime.date(year_int, month_int, day_int)
        if 0 <= hour < 8:
            base_date = base_date + jdatetime.timedelta(days=1)

        # همگام‌سازی year/month/day با تاریخ جدید
        self.year = f"{base_date.year:04d}"
        self.month = f"{base_date.month:02d}"
        self.day = f"{base_date.day:02d}"

        self.timestamp = int(
            jdatetime.datetime(
                year=base_date.year,
                month=base_date.month,
                day=base_date.day,
                hour=hour,
                minute=minute,
            )
            .togregorian()
            .timestamp()
        )

        # par10 = par05 + par51
        if self.par05 != "Not Tested" and self.par51 != "Not Tested":
            self.par10 = str(Decimal(self.par05) + Decimal(self.par51))
        else:
            self.par10 = "Not Tested"

        # par16 = 100 - par10 - par60
        if self.par10 != "Not Tested" and self.par60 != "Not Tested":
            self.par16 = str(Decimal("100.0") - Decimal(self.par10) - Decimal(self.par60))
        else:
            self.par16 = "Not Tested"


# Example :

# result = LabResult(
#     year="1402",
#     month="01",
#     day="24",
#     time="1330",
#     klin1="1.32",
#     klin2="3.42",
#     above40=Decimal("12.5"),
#     par05=Decimal("0.5"),
#     par51=Decimal("1.1"),
#     # par10=Decimal("2.0"), نیازی به وارد کردن این قسمت نیست
#     # par16=Decimal("1.6"), نیازی به وارد کردن این قسمت نیست
#     par60=Decimal("6.0"),
# )
# print(result.model_dump())


# Result:

# result = {
#     "timestamp": 1710410400,
#     "year": "1402",
#     "month": "01",
#     "day": "24",
#     "time": "1330",
#     "klin1": "1.32",
#     "klin2": "3.42",
#     "above40": "12.50",
#     "par05": "0.5",
#     "par51": "1.1",
#     "par10": "1.6",
#     "par16": "92.4",
#     "par60": "6.0",
# }
