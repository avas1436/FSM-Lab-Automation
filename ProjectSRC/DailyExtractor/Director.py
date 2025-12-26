import csv
import os
import sqlite3
from abc import ABC, abstractmethod
from decimal import Decimal

import toml  # type: ignore
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
    pass


data = LabResult(
    sampleID="5cdd6790-e061-4009-8f27-2e90b3efb0be",
    year="1404",
    month="07",
    day="01",
    time="0800",
    timestamp=1758601800,
    klin1=Decimal("4.72"),
    klin2=Decimal("3.36"),
    above40=Decimal("2.35"),
    par05=Decimal("3.9"),
    par51=Decimal("3.7"),
    par10=Decimal("7.6"),
    par16=Decimal("92.4"),
    par60=Decimal("0.0"),
)


with CsvSaver() as saver:
    saver.save(data=data)
