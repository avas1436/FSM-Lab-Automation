import datetime
from abc import ABC
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any, Dict

import pandas as pd  # type: ignore
from openpyxl import load_workbook  # type: ignore
from Product import LabResult  # type: ignore


# Interface
class ExcelAdapter(ABC):
    """یک کلاس پایه که همه ادپتر های زیر مجموعه باید از آن ارث ببرند"""

    def get_records(self):
        raise NotImplementedError


# Adapter with openpyxl
class Openpyxl(ExcelAdapter):
    """لود کردن دیتا در رم به صورت یکجا"""

    def __init__(self, file_path: str, start: int, end: int):
        self.file_path = file_path
        self.start = start
        self.end = end

    def get_records(self):
        wb = load_workbook(filename=rf"{self.file_path}", data_only=True, read_only=True)
        sheet_names = wb.sheetnames
        active_sheets = sheet_names[self.start - 1 : self.end]
        for sheet in active_sheets:
            ws = wb[sheet]
            cell_range = ws["A4":"L31"]

            sheet_data = [[cell.value for cell in ls] for ls in cell_range]

            yield sheet_data

        wb.close()


# Adapter with pandas
class Pandas(ExcelAdapter):

    def __init__(self, file_path: str, start: int, end: int):
        self.file_path = file_path
        self.start = start
        self.end = end

    def get_records(self):
        # خواندن کل فایل اکسل
        xls = pd.ExcelFile(self.file_path)
        sheet_names = xls.sheet_names
        active_sheets = sheet_names[self.start - 1 : self.end]
        for sheet in active_sheets:
            # خواندن محدوده‌ی سلول‌ها (A4:L31) # skiplss=3 یعنی از ردیف چهارم شروع کند (چون اندیس از 0 است)
            df = pd.read_excel(
                self.file_path,
                sheet_name=sheet,
                header=None,
                skiplss=3,  # شروع از ردیف 4
                nlss=28,  # تا ردیف 31 (31-4+1 = 28 ردیف)
                usecols="A:L",  # ستون‌های A تا L
            )

        # تبدیل به لیست لیست‌ها مثل خروجی openpyxl
        sheet_data = df.values.tolist()

        yield sheet_data


# Facade
class ExcelAdapterFacade:
    def __init__(self, file_path: str, start: int = 1, end: int = 31, engine: str = "openpyxl"):
        if engine == "openpyxl":
            self.adapter = Openpyxl(file_path=file_path, start=start, end=end)
        elif engine == "pandas":
            self.adapter = Pandas(file_path=file_path, start=start, end=end)  # type: ignore
        else:
            raise ValueError("Engine must be 'pandas' or 'openpyxl'")

    def get_records(self):
        return self.adapter.get_records()


def safe_decimal(value, sp: str = "0.1") -> Decimal | str:
    if value is None:
        return "Not Tested"
    try:
        return Decimal(str(value)).quantize(Decimal(sp), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return "Not Tested"


class LabResultBuilder:
    def __init__(self, raw_data: list[list]):
        self.raw_data = raw_data
        self._records: list[dict[str, Any]] = []

    def parse(self):
        date = self.raw_data[0][4]  # '1404/07/02'
        year, month, day = str(date).split("/")

        for i, ls in enumerate(self.raw_data):

            if i < 8:
                continue

            if isinstance(ls[0], (datetime.time, datetime.datetime)):
                time = ls[0].strftime("%H%M")
            else:
                continue

            record = {
                "year": year,
                "month": month,
                "day": day,
                "time": time,
                "klin1": safe_decimal(str(ls[1]), sp="0.01") if ls[1] is not None else "Not Tested",
                "klin2": safe_decimal(str(ls[3]), sp="0.01") if ls[3] is not None else "Not Tested",
                "above40": (
                    safe_decimal(str(ls[5]), sp="0.01") if ls[5] is not None else "Not Tested"
                ),
                "par05": (
                    safe_decimal(str(self.raw_data[i + 1][8]))
                    if 7 < i < 20 and self.raw_data[i + 1][8] is not None
                    else "Not Tested"
                ),
                "par51": (
                    safe_decimal(str(self.raw_data[i + 1][9]))
                    if 7 < i < 20 and self.raw_data[i + 1][9] is not None
                    else "Not Tested"
                ),
                "par60": safe_decimal(str(ls[11])) if ls[11] is not None else "Not Tested",
            }

            fields = ["klin1", "klin2", "above40", "par05"]
            if all(record[f] == "Not Tested" for f in fields):
                continue

            self._records.append(record)

        return self

    def build(self) -> list[LabResult]:
        return [LabResult(**rec) for rec in self._records]


# openpyxl adaptor test:

# excel = Openpyxl(
#     file_path=r"C:\Users\abAsz\Documents\GIT\FSM Lab Automation\ProjectSRC\DailyExtractor\daily.xlsx",
#     start=1,
#     end=4,
# )

# data = excel.get_records()

# for i in range(4):
#     data_parser = LabResultBuilder(next(data))
#     lab_result = data_parser.parse().build()
#     print(lab_result)
