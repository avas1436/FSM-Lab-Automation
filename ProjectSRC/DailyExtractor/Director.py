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
    def save(self, data):
        return super().save(data)


class TomlSaver(Saver):
    def save(self, data):
        return super().save(data)


class SqliteSaver(Saver):
    def save(self, data):
        return super().save(data)


# Director - from Builder Pattern
class LabResultManager:
    pass
