# import sqlite3
# import toml  # type: ignore
from pydantic import BaseModel

from ProjectSRC.DailyExtractor.Builder import (  # type: ignore
    ExcelAdapterFacade,
    LabResultBuilder,
)
from ProjectSRC.DailyExtractor.Saver import (  # type: ignore
    CsvSaver,
    SqliteSaver,
    TomlSaver,
)
from ProjectSRC.Logger.logger_config import logger


# Director - from Builder Pattern
class LabResultManager(BaseModel):
    """This class receives input parameters, manages data extraction,
    and saves results without requiring external knowledge of its internals."""

    daily_file: str = "daily.xlsx"
    start_day: int = 1
    end_day: int = 31
    extract_engine: str = "openpyxl"
    excel_data: list[list] = []
    saver_engine: str = "csv"
    output: str = r"DataBase\csvdatabase.csv"

    def _extract_data(self):
        logger.info(
            "Starting data extraction from %s using engine=%s",
            self.daily_file,
            self.extract_engine,
        )
        facade = ExcelAdapterFacade(
            file_path=self.daily_file,
            start=self.start_day,
            end=self.end_day,
            engine=self.extract_engine,
        )
        self.excel_data = list(facade.get_records())
        logger.debug(f"Extracted {len(self.excel_data)} records successfully")
        return self.excel_data

    def _select_saver(self):
        # logger.info(f"Selecting saver engine: {self.saver_engine}")
        if self.saver_engine == "csv":
            return CsvSaver(file_path=self.output)

        if self.saver_engine == "toml":
            return TomlSaver(file_path=self.output)

        if self.saver_engine == "sqlite3":
            return SqliteSaver(file_path=self.output)

        else:
            logger.critical(f"Unsupported saver engine: {self.saver_engine}")
            raise ValueError("Unsupported database engine")

    def save_results(self):
        # logger.info("Initiating save_results workflow")
        saver = self._select_saver()
        self._extract_data()

        if isinstance(saver, CsvSaver):
            with saver as s:
                # logger.info("Saving results to CSV at %s", self.output)
                for day_index, days in enumerate(self.excel_data, start=1):
                    logger.debug(f"Processing day {day_index} with {len(days)} entries")
                    data_parser_object = LabResultBuilder(days)
                    lab_result = data_parser_object.parse().build()
                    for record_index, data in enumerate(lab_result, start=1):
                        # logger.debug(f"Saving record {record_index}: {data}")
                        s.save(data)

                logger.info(f"All results saved successfully to {self.output}")


if __name__ == "__main__":
    m = LabResultManager(
        daily_file=r"C:\Users\abAsz\Documents\Foolad-Sang-Automation\4. data extract\استخراج دیتا گزارش روزانه\7\daily.xlsx",
        start_day=1,
        end_day=31,
    )
    m.save_results()
