from abc import ABC

from openpyxl import load_workbook


class ExcelAdapter(ABC):
    """یک کلاس پایه که همه ادپتر های زیر مجموعه باید از آن ارث ببرند"""

    def get_records(self):
        raise NotImplementedError


class Openpyxl(ExcelAdapter):
    """لود کردن دیتا در رم به صورت یکجا"""

    def __init__(self, file_path: str = "daily.xlsx", start: int = 1, end: int = 31):
        self.file_path = file_path
        self.start = start
        self.end = end

    def get_records(self):
        pass


class Pandas(ExcelAdapter):
    def get_records(self):
        return super().get_records()


class LabResultBuilder:
    pass
