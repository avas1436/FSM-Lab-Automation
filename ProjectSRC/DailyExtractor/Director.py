import csv
import sqlite3
from abc import ABC, abstractmethod

import toml  # type: ignore

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

    def __enter__(self):
        self.out_file = open(file=self.file_path, mode="w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.out_file, delimiter="|")
        return self

    def save(self, data):
        self.csv_writer.writerow(data.dict().values())
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
