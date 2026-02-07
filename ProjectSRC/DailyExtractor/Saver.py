import csv
import os
import toml  # type: ignore
from abc import ABC, abstractmethod
from typing import Self

# Srategy pattern


# --- Strategy Interface ---
class Saver(ABC):
    @abstractmethod
    def save(self, data) -> Self:
        pass


# --- Concrete Strategies ---
class CsvSaver(Saver):
    def __init__(self, file_path: str = r"DataBase\csvdatabase.csv"):
        self.file_path = file_path
        self.out_file = None
        self.csv_writer = None

    def __enter__(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # write in csv file in append mode in this mode previous data will be preserved
        file_exists = os.path.exists(self.file_path)
        self.out_file = open(self.file_path, mode="a", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.out_file, delimiter=",")

        # if file is empty or not exists write header
        if not file_exists or os.path.getsize(self.file_path) == 0:
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

        return self

    def save(self, data) -> Self:
        assert self.csv_writer is not None
        self.csv_writer.writerow(data.model_dump().values())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.out_file:
            self.out_file.close()


# --- Concrete Strategies ---
class TomlSaver(Saver):
    def __init__(self, file_path: str = r"DataBase\tomldatabase.toml"):
        self.file_path = file_path
        self._data: dict[str, list[dict]] = {"records": []}

    def __enter__(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            self._data = toml.load(self.file_path)
            if "records" not in self._data or not isinstance(
                self._data["records"], list
            ):
                self._data["records"] = []

        return self

    def save(self, data) -> Self:
        self._data["records"].append(data.model_dump())
        with open(self.file_path, mode="w", encoding="utf-8") as out_file:
            toml.dump(self._data, out_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None


# --- Concrete Strategies ---
class SqliteSaver(Saver):
    def save(self, data):
        return super().save(data)


class Strategy_fecade:
    pass
