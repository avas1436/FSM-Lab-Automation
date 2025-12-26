import csv
import os
import sqlite3
from abc import ABC, abstractmethod
from decimal import Decimal

import toml  # type: ignore
import typer
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


app = typer.Typer(add_completion=False)


def interactive():

    def _validate_days(start: int, end: int) -> None:
        if start < 1 or end < start:
            raise typer.BadParameter(message="Invalid day range. Must satisfy 1 <= start <= end.")

    typer.secho(
        message="LabResultManager",
        fg=typer.colors.CYAN,
        bold=True,
    )

    # Always prompt the user for each parameter (100% interactive behavior).
    daily_file = typer.prompt(text="Enter path to daily Excel file", default="daily.xlsx")
    start_day = typer.prompt(text="Enter start day (integer)", default=1, type=int)
    end_day = typer.prompt(text="Enter end day (integer)", default=31, type=int)

    try:
        _validate_days(start=start_day, end=end_day)
    except typer.BadParameter as exc:
        typer.secho(message=f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    engine = typer.prompt(text="Enter Excel processing engine (e.g. openpyxl)", default="openpyxl")
    db = typer.prompt(text="Enter database engine (csv | toml | sqlite3)", default="csv")
    output = typer.prompt(text="Enter output path", default=r"DataBase\csvdatabase.csv")

    typer.secho(message="\n=== Selected configuration ===", fg=typer.colors.GREEN, bold=True)
    typer.echo(message=f"Excel file : {daily_file}")
    typer.echo(message=f"Days       : {start_day} -> {end_day}")
    typer.echo(message=f"Engine     : {engine}")
    typer.echo(message=f"DB engine  : {db}")
    typer.echo(message=f"Output     : {output}")
    typer.secho(message="=============================\n", fg=typer.colors.GREEN)

    if not typer.confirm(text="Do you want to continue?"):
        typer.secho(message="Operation cancelled by user.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    # Instantiate and run manager (adjust imports/names to your project)
    try:
        mgr = LabResultManager(
            daily_file=daily_file,
            start_day=start_day,
            end_day=end_day,
            proccess_engine=engine,
            database_engine=db,
            output=output,
        )

        typer.secho(message="Processing and saving results...", fg=typer.colors.BLUE)

        # Prefer calling manager's own save_results if available.
        try:
            result = mgr.save_results()
            if isinstance(result, int):
                typer.secho(message=f"Done. Records saved: {result}", fg=typer.colors.GREEN)
            else:
                typer.secho(message="Done. Processing finished.", fg=typer.colors.GREEN)
        except AttributeError:
            # Fallback: manual processing using _select_saver and excel_data
            if not hasattr(mgr, "_select_saver"):
                typer.secho(
                    message="Error: LabResultManager does not provide save_results or _select_saver.",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(code=2)

            saver = mgr._select_saver()
            processed = 0
            with saver as s:
                # If mgr._excel_data is a generator, use it; otherwise iterate mgr.excel_data
                try:
                    source = mgr._excel_data()
                except Exception:
                    source = getattr(mgr, "excel_data", [])

                for record in source:
                    # If your implementation yields the manager itself, try to extract the record
                    if isinstance(record, LabResultManager):
                        record = getattr(record, "excel_data", None)

                    data_parser = LabResultBuilder(raw_data=record)
                    lab_result = data_parser.parse().build()
                    for data in lab_result:
                        s.save(data=data)
                        processed += 1

            typer.secho(message=f"Done. Records saved: {processed}", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(message=f"Execution error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
    # m = LabResultManager(
    #     daily_file=r"C:\Users\abAsz\Documents\GIT\FSM Lab Automation\ProjectSRC\DailyExtractor\daily.xlsx"
    # )
    # m.save_results()
