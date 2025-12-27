# import sqlite3
# import toml  # type: ignore
from Builder import ExcelAdapterFacade, LabResultBuilder  # type: ignore
from pydantic import BaseModel
from Saver import CsvSaver, SqliteSaver, TomlSaver  # type: ignore


# Director - from Builder Pattern
class LabResultManager(BaseModel):
    """این کلاس تنها اطلاعات را میگیرد و خودش تمامی دیتای مورد نیاز را
    ذخیره میکند و هیچ نیازی به دانستن جزییات کارش نیس"""

    daily_file: str = "daily.xlsx"
    start_day: int = 1
    end_day: int = 31
    extract_engine: str = "openpyxl"
    excel_data: list[list] = []
    saver_engine: str = "csv"
    output: str = r"DataBase\csvdatabase.csv"

    def _extract_data(self):
        facade = ExcelAdapterFacade(
            file_path=rf"{self.daily_file}",
            start=self.start_day,
            end=self.end_day,
            engine=self.extract_engine,
        )
        records = facade.get_records()
        for sheet_data in records:
            self.excel_data = sheet_data
            yield self

    def _select_saver(self):
        if self.saver_engine == "csv":
            return CsvSaver(file_path=self.output)

        if self.saver_engine == "toml":
            return TomlSaver(file_path=self.output)

        if self.saver_engine == "sqlite3":
            return SqliteSaver(file_path=self.output)

        else:
            raise ValueError("Unsupported database engine")

    def save_results(self):
        saver = self._select_saver()

        if isinstance(saver, CsvSaver):
            with saver as s:
                for record in self.excel_data:
                    data_parser = LabResultBuilder(raw_data=record)
                    lab_result = data_parser.parse().build()
                    for data in lab_result:
                        s.save(data=data)


if __name__ == "__main__":
    m = LabResultManager(daily_file=r"F:\گزارش\1404\9. آذر\daily.xlsx")
    m.save_results()
