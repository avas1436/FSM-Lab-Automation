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
            file_path=self.daily_file,
            start=self.start_day,
            end=self.end_day,
            engine=self.extract_engine,
        )
        self.excel_data = list(facade.get_records())
        return self.excel_data

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
        self._extract_data()

        if isinstance(saver, CsvSaver):
            with saver as s:
                for days in self.excel_data:
                    data_parser_object = LabResultBuilder(days)
                    lab_result = data_parser_object.parse().build()
                    for data in lab_result:
                        s.save(data)


if __name__ == "__main__":
    m = LabResultManager(
        daily_file=r"C:\Users\abAsz\Documents\Foolad-Sang-Automation\4. data extract\استخراج دیتا گزارش روزانه\5\daily.xlsx",
        start_day=1,
        end_day=31,
    )
    m.save_results()
