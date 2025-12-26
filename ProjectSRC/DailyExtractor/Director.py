import csv
import os
import sqlite3
from abc import ABC, abstractmethod
from decimal import Decimal

import toml  # type: ignore
from Builder import ExcelAdapterFacade, LabResultBuilder, Openpyxl, Pandas  # type: ignore
from genericpath import exists
from Product import LabResult  # type: ignore

# Srategy pattern


# --- Strategy Interface ---
class Saver(ABC):
    @abstractmethod
    def save(self, data):
        pass


# --- Concrete Strategies ---
class CsvSaver(Saver):
    def __init__(self, file_path: str = r"DataBase\csvdatabase.csv"):
        self.file_path = file_path
        self.out_file = None
        self.csv_writer = None
        self.header_written = False

    def __enter__(self):

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        self.out_file = open(file=self.file_path, mode="w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.out_file, delimiter=",")

        # نوشتن هدر فقط یک بار
        if not self.header_written:
            self.csv_writer.writerow(
                [
                    "Time Stamp",
                    "Year",
                    "Month",
                    "Day",
                    "Time",
                    "Klin 1",
                    "Klin 2",
                    "Above 40mm CO2",
                    "particles 0-5mm",
                    "particles 5-10mm",
                    "particles 0-10mm",
                    "particles 10-60mm",
                    "particles +60mm",
                ]
            )
            self.header_written = True

        return self

    def save(self, data):
        self.csv_writer.writerow(data.model_dump().values())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.out_file:
            self.out_file.close()


class TomlSaver(Saver):
    def save(self, data):
        return super().save(data)


class SqliteSaver(Saver):
    def save(self, data):
        return super().save(data)


# Director - from Builder Pattern
class LabResultManager:
    def __init__(
        self,
        daily_file: str = "daily.xlsx",
        start_day: int = 1,
        end_day: int = 31,
        proccess_engine: str = "openpyxl",
        excel_data=None,
        database_engine: str = "csv",
        output: str = r"DataBase\csvdatabase.csv",
    ):
        self.daily_file = daily_file
        self.start_day = start_day
        self.end_day = end_day
        self.proccess_engine = proccess_engine
        self.engine = ExcelAdapterFacade(
            file_path=rf"{self.daily_file}",
            start=self.start_day,
            end=self.end_day,
            engine=self.proccess_engine,
        )
        self.excel_data = self.engine.get_records()
        self.database_engine = database_engine
        self.output = output

    def _excel_data(self):
        for ـ in range(self.end_day - self.start_day + 1):
            self.excel_data = next(self.engine)
            yield self

    def _select_saver(self):
        if self.database_engine == "csv":
            return CsvSaver(file_path=self.output)

        if self.database_engine == "toml":
            return TomlSaver(file_path=self.output)

        if self.database_engine == "sqlite3":
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
                        saver.save(data=data)


if __name__ == "__main__":
    m = LabResultManager(
        daily_file=r"C:\Users\abAsz\Documents\GIT\FSM Lab Automation\ProjectSRC\DailyExtractor\daily.xlsx"
    )
    m.save_results()
