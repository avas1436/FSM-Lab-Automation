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
    timestamp: int | str = "NA"
    klin1: Decimal | str = "Not Tested"
    klin2: Decimal | str = "Not Tested"
    above40: Decimal | str = "Not Tested"
    par05: Decimal | str = "Not Tested"
    par51: Decimal | str = "Not Tested"
    par10: Decimal | str = "Not Tested"
    par16: Decimal | str = "Not Tested"
    par60: Decimal | str = "Not Tested"

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
        """بعد از ساخت مدل، فیلدهای محاسباتی را مقداردهی کن"""

        # timestamp از تاریخ شمسی ساخته می‌شود
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

        # par10 = par05 + par51
        if isinstance(self.par05, Decimal) and isinstance(self.par51, Decimal):
            self.par10 = self.par05 + self.par51
        else:
            self.par10 = "Not Tested"
        # self.par10 = self.par05 + self.par51  # type: ignore

        # par16 = 100 - par10 - par60
        if isinstance(self.par10, Decimal) and isinstance(self.par60, Decimal):
            self.par16 = Decimal("100.0") - self.par10 - self.par60
        else:
            self.par16 = "Not Tested"
        # self.par16 = Decimal("100.0") - self.par10 - self.par60  # type: ignore


# Example :

# result = LabResult(
#     year="1402",
#     month="12",
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
# print(result)


# Result:

# result = sampleID='73796d9c-3b75-461f-ae3b-1de2ad3a7076'
# year='1402'
# month='12'
# day='24'
# time='1330'
# timestamp=1710410400
# klin1=Decimal('1.32')
# klin2=Decimal('3.42')
# above40=Decimal('12.5')
# par05=Decimal('0.5')
# par51=Decimal('1.1')
# par10=Decimal('1.6')
# par16=Decimal('92.4')
# par60=Decimal('6.0')
