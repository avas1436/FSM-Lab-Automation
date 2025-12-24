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
    klin: int
    above40: Decimal | str = "Not Tested"
    carbondioxide: Decimal | str = "Not Tested"
    par05: Decimal | str = "Not Tested"
    par51: Decimal | str = "Not Tested"
    par10: Decimal | str = "Not Tested"
    par16: Decimal | str = "Not Tested"
    par60: Decimal | str = "Not Tested"

    @field_validator("klin", mode="before")
    def check_klin(cls, v):
        allowed = {1, 2, 12}
        if int(v) not in allowed:
            raise ValueError("klin must be one of 1, 2, or 12")
        return int(v)

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
        self.par10 = self.par05 + self.par51  # type: ignore

        # par16 = 100 - par10 - par60
        self.par16 = Decimal("100.0") - self.par10 - self.par60  # type: ignore


# Example :

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
#     # par10=Decimal("2.0"), نیازی به وارد کردن این قسمت نیست
#     # par16=Decimal("1.6"), نیازی به وارد کردن این قسمت نیست
#     par60=Decimal("6.0"),
# )
# print(result)


# Result:

# result = sampleID='7c70773e-81c3-4f91-b3be-b2924892db0d'
#    year='1402'
#    month='12'
#    day='24'
#    time='1330'
#    timestamp=1710410400
#    klin=1
#    above40=Decimal('12.5')
#    carbondioxide=Decimal('3.2')
#    par05=Decimal('0.5')
#    par51=Decimal('1.1')
#    par10=Decimal('1.6')
#    par16=Decimal('92.4')
#    par60=Decimal('6.0')
