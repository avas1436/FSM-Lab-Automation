from abc import ABC

from openpyxl import load_workbook


class ExcelAdapter(ABC):
    """یک کلاس پایه که همه ادپتر های زیر مجموعه باید از آن ارث ببرند"""

    def get_records(self):
        raise NotImplementedError


class Openpyxl(ExcelAdapter):
    def get_records(self):
        return super().get_records()


class Pandas(ExcelAdapter):
    def get_records(self):
        return super().get_records()


class LabResultBuilder:
    pass
