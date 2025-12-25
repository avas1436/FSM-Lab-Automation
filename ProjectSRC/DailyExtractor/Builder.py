from abc import ABC

from openpyxl import load_workbook  # type: ignore


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
        wb = load_workbook(filename=rf"{self.file_path}", data_only=True, read_only=True)
        sheet_names = wb.sheetnames
        active_sheets = sheet_names[self.start - 1 : self.end]
        for sheet in active_sheets:
            ws = wb[sheet]
            cell_range = ws["A4":"L31"]

            sheet_data = [[cell.value for cell in row] for row in cell_range]

            yield sheet_data

        wb.close()


class Pandas(ExcelAdapter):
    def get_records(self):
        return super().get_records()


class LabResultBuilder:
    pass


# openpyxl adaptor test:


# excel = Openpyxl(
#     file_path=r"C:\Users\abAsz\Documents\GIT\FSM Lab Automation\ProjectSRC\DailyExtractor\daily.xlsx",
#     start=1,
#     end=4,
# )

# data = excel.get_records()
# for i in range(4):
#     print(next(data))
