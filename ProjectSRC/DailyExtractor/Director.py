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
        logger.debug("Extracted %d records successfully", len(self.excel_data))
        return self.excel_data

    def _select_saver(self):
        logger.info("Selecting saver engine: %s", self.saver_engine)
        if self.saver_engine == "csv":
            return CsvSaver(file_path=self.output)

        if self.saver_engine == "toml":
            return TomlSaver(file_path=self.output)

        if self.saver_engine == "sqlite3":
            return SqliteSaver(file_path=self.output)

        else:
            logger.critical("Unsupported saver engine: %s", self.saver_engine)
            raise ValueError("Unsupported database engine")

    def save_results(self):
        logger.info("Initiating save_results workflow")
        saver = self._select_saver()
        self._extract_data()

        if isinstance(saver, CsvSaver):
            with saver as s:
                logger.info("Saving results to CSV at %s", self.output)
                for day_index, days in enumerate(self.excel_data, start=1):
                    logger.debug(
                        "Processing day %d with %d entries", day_index + 1, len(days)
                    )
                    data_parser_object = LabResultBuilder(days)
                    lab_result = data_parser_object.parse().build()
                    for record_index, data in enumerate(lab_result, start=1):
                        logger.debug("Saving record #%d: %s", record_index + 1, data)
                        s.save(data)

                logger.info("All results saved successfully to %s", self.output)


# if __name__ == "__main__":
#     m = LabResultManager(
#         daily_file=r"F:\گزارش\1404\3. خرداد\daily.xlsx",
#         start_day=1,
#         end_day=31,
#     )
#     m.save_results()
