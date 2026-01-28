# from Director import LabResultManager  # type: ignore
from InquirerPy import inquirer
from pydantic import BaseModel


class InteractiveLabResultManager(BaseModel):
    """Interactive CLI for extract and save LabResult"""

    daily_file: str
    start_day: int = 1
    end_day: int = 31
    extract_engine: str
    excel_data: list[list] = []
    saver_engine: str
    output: str

    def _show_welcome(self):
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        MAGENTA = "\033[95m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

        print()
        print(BOLD + CYAN + "=" * 70 + RESET)
        print(BOLD + MAGENTA + "              Lab Result Manager              " + RESET)
        print(BOLD + CYAN + "=" * 70 + RESET)
        print()

        print(
            GREEN
            + "An interactive CLI tool for extracting data from daily IS lab reports"
            + RESET
        )
        print(
            GREEN
            + "and saving structured lab results into Excel or other output formats."
            + RESET
        )
        print()

        print(BOLD + YELLOW + "Parameters Overview:" + RESET)
        print(
            BLUE
            + "• daily_file"
            + RESET
            + "     : Path or pattern for daily lab report files"
        )
        print(
            BLUE
            + "• start_day"
            + RESET
            + "      : First day of the month to start extraction"
        )
        print(
            BLUE
            + "• end_day"
            + RESET
            + "        : Last day of the month to stop extraction"
        )
        print(
            BLUE
            + "• extract_engine"
            + RESET
            + " : Engine responsible for parsing and extracting data"
        )
        print(
            BLUE
            + "• saver_engine"
            + RESET
            + "   : Engine used to persist data to the output"
        )
        print(
            BLUE + "• output" + RESET + "        : Destination path for saved results"
        )
        print()

        print(BOLD + CYAN + "=" * 70 + RESET)
        print()

    def _get_daily_file(self):
        self.daily_file = inquirer.text(
            message="Enter the path to the daily lab Excel file: ",
            default="daily.xlsx",
        ).execute()

    def _get_date_range(self):
        self.start_day = inquirer.number(
            message="Enter the start day of the month:",
            min_allowed=1,
            max_allowed=31,
            default=self.start_day,
        ).execute()

        self.end_day = inquirer.number(
            message="Enter the end day of the month:",
            min_allowed=self.start_day,
            max_allowed=31,
            default=self.end_day,
        ).execute()

    def _get_extract_engine(self):
        # Step 3: Select extraction engine
        self.extract_engine = inquirer.fuzzy(
            message="Select the extraction engine to use: ",
            choices=["openpyxl", "pandas"],
        ).execute()

    def _get_saver_engine(self):
        # Step 4: Select saving format
        self.saver_engine = inquirer.fuzzy(
            message="Select the output storage format: ",
            choices=["csv", "toml", "sqlite3"],
        ).execute()

    def _get_output_path(self):
        use_default = inquirer.confirm(
            message="Would you like to use the default output path?"
        ).execute()

        if use_default:
            default_paths = {
                "csv": r"DataBase\csvdatabase.csv",
                "toml": r"DataBase\tomldatabase.toml",
                "sqlite3": r"DataBase\sqlitedatabase.db",
            }
            self.output = default_paths[self.saver_engine]
        else:
            self.output = inquirer.text(
                message="Please enter the output file path:",
            ).execute()

    def _confirm_configuration(self) -> bool:
        return inquirer.confirm(
            message="Do you want to start processing with the selected configuration?"
        ).execute()

    def _run_processing(self):
        pass
        # Starting processing...

        # manager = LabResultManager(
        #     daily_file=self.config["daily_file"],
        #     start_day=self.config["start_day"],
        #     end_day=self.config["end_day"],
        #     extract_engine=self.config["extract_engine"],
        #     saver_engine=self.config["saver_engine"],
        #     output=self.config["output"],
        # )

        # Processing completed successfully!

        # except Exception as e:
        #     Error during processing:

    def run(self):
        #     try:
        #         while True:
        #             self._show_welcome()
        #             self._get_daily_file()
        #             self._get_date_range()
        #             self._get_extract_engine()
        #             self._get_saver_engine()
        #             self._get_output_path()
        # except KeyboardInterrupt:
        # Program interrupted by user.
        # except Exception as e:
        # Unexpected error:

        # Thank you for using Lab Result Manager!

        pass


if __name__ == "__main__":
    manager = InteractiveLabResultManager()

    manager._show_welcome()
    manager._get_date_range()
    manager._get_saver_engine()
    manager._get_daily_file()
