import sys
from pathlib import Path
from typing import Any

import questionary
from Builder import ExcelAdapterFacade, LabResultBuilder
from Manager import LabResultManager  # make sure this import points to your Manager file
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from Saver import CsvSaver, SqliteSaver, TomlSaver


class InteractiveLabResultManager:
    """Interactive CLI for managing lab results with a clean English interface."""

    def __init__(self):
        self.console = Console()
        self.config = {}

    def _show_welcome(self):
        self.console.clear()
        self.console.print(
            Panel.fit(
                "[bold cyan]🏥 Lab Result Manager[/bold cyan]\n"
                "[italic]Manage and save lab results[/italic]",
                border_style="cyan",
            )
        )

    def _show_config_summary(self):
        table = Table(title="Configuration Summary", title_style="bold green")
        table.add_column("Parameter", style="cyan", width=20)
        table.add_column("Value", style="yellow", width=40)

        for key, value in self.config.items():
            table.add_row(key, str(value))

        self.console.print(Panel(table, border_style="green"))

    def _get_daily_file(self):
        self.console.print("\n[bold]📁 Step 1: Select Excel file[/bold]")

        excel_files = list(Path(".").glob("*.xlsx")) + list(Path(".").glob("*.xls"))

        choices = []
        if excel_files:
            choices = [
                questionary.Choice(title=f"📄 {file.name}", value=str(file))
                for file in excel_files[:5]
            ]

        choices.extend(
            [
                questionary.Choice(title="📁 Enter file path manually", value="manual"),
                questionary.Choice(title="Use daily.xlsx (default)", value="daily.xlsx"),
            ]
        )

        selection = questionary.select(
            "Choose the daily Excel file:", choices=choices, use_shortcuts=True
        ).ask()

        if selection == "manual":
            file_path = questionary.text("Enter full Excel file path:", default="daily.xlsx").ask()
            self.config["daily_file"] = file_path
        else:
            self.config["daily_file"] = selection

    def _get_date_range(self):
        self.console.print("\n[bold]📅 Step 2: Select day range[/bold]")

        start_day = IntPrompt.ask("Enter start day", default=1, show_default=True)
        end_day = IntPrompt.ask("Enter end day", default=31, show_default=True)

        while end_day < start_day:
            self.console.print("[red]❌ End day must be >= start day![/red]")
            end_day = IntPrompt.ask("Re-enter end day", default=31)

        self.config["start_day"] = start_day
        self.config["end_day"] = end_day

    def _get_extract_engine(self):
        self.console.print("\n[bold]⚙️ Step 3: Select extraction engine[/bold]")

        engine = questionary.select(
            "Choose Excel processing engine:",
            choices=[
                questionary.Choice("openpyxl (default)", value="openpyxl"),
                questionary.Choice("pandas", value="pandas"),
            ],
            default="openpyxl",
        ).ask()

        self.config["extract_engine"] = engine

    def _get_saver_engine(self):
        self.console.print("\n[bold]💾 Step 4: Select saving format[/bold]")

        choices = [
            questionary.Choice("📊 CSV - simple readable file", value="csv"),
            questionary.Choice("⚙️ TOML - structured config format", value="toml"),
            questionary.Choice("🗄️ SQLite3 - lightweight database", value="sqlite3"),
        ]

        saver_engine = questionary.select(
            "Choose saving format:", choices=choices, default="csv"
        ).ask()

        self.config["saver_engine"] = saver_engine

    def _get_output_path(self):
        self.console.print("\n[bold]📂 Step 5: Select output path[/bold]")

        default_paths = {
            "csv": r"DataBase\csvdatabase.csv",
            "toml": r"DataBase\tomldatabase.toml",
            "sqlite3": r"DataBase\sqlitedatabase.db",
        }

        default_output = default_paths.get(
            self.config.get("saver_engine", "csv"), r"DataBase\output"
        )

        Path("DataBase").mkdir(exist_ok=True)

        output = questionary.text(
            "Enter output file path:",
            default=default_output,
            validate=lambda x: len(x) > 0 or "Path cannot be empty",
        ).ask()

        self.config["output"] = output

    def _confirm_configuration(self) -> bool:
        self.console.print("\n" + "=" * 60)
        self._show_config_summary()

        return Confirm.ask(
            "\n[bold yellow]Do you want to start processing?[/bold yellow]", default=True
        )

    def _run_processing(self):
        try:
            self.console.print("\n[bold green]🚀 Starting processing...[/bold green]")

            manager = LabResultManager(
                daily_file=self.config["daily_file"],
                start_day=self.config["start_day"],
                end_day=self.config["end_day"],
                extract_engine=self.config["extract_engine"],
                excel_data=[],
                saver_engine=self.config["saver_engine"],
                output=self.config["output"],
            )

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=False,
            ) as progress:
                task = progress.add_task(
                    f"Processing days {self.config['start_day']} to {self.config['end_day']}...",
                    total=self.config["end_day"] - self.config["start_day"] + 1,
                )

                manager.save_results()
                progress.update(task, completed=progress.tasks[task].total)

            self.console.print(f"\n[bold green]✅ Processing completed successfully![/bold green]")
            self.console.print(f"[cyan]📁 Output file: {self.config['output']}[/cyan]")

        except Exception as e:
            self.console.print(f"\n[red]❌ Error during processing:[/red] {str(e)}")
            return False

        return True

    def run(self):
        try:
            while True:
                self._show_welcome()
                self._get_daily_file()
                self._get_date_range()
                self._get_extract_engine()
                self._get_saver_engine()
                self._get_output_path()

                if self._confirm_configuration():
                    success = self._run_processing()
                    if success:
                        break
                else:
                    retry = Confirm.ask(
                        "[yellow]Do you want to change configuration?[/yellow]", default=True
                    )
                    if not retry:
                        break

        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️ Program interrupted by user.[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Unexpected error:[/red] {str(e)}")

        self.console.print("\n[cyan]👋 Thank you for using Lab Result Manager![/cyan]")


if __name__ == "__main__":
    app = InteractiveLabResultManager()
    app.run()
