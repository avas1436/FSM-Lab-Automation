# from Director import LabResultManager  # type: ignore
from InquirerPy import inquirer


class InteractiveLabResultManager:
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
        # Step 1: Select Excel file
        pass

    def _get_date_range(self):
        self.start_day = inquirer.number(
            message="Enter start day:",
            default=1,
        ).execute()
        self.start_day = int(self.start_day)
        self.end_day = inquirer.number(
            message="Enter end day:",
            default=31,
        ).execute()
        self.end_day = int(self.end_day)

    def _get_extract_engine(self):
        # Step 3: Select extraction engine
        pass

    def _get_saver_engine(self):
        # Step 4: Select saving format
        pass

    def _get_output_path(self):
        # Step 5: Select output path

        # default_paths = {
        #     "csv": r"DataBase\csvdatabase.csv",
        #     "toml": r"DataBase\tomldatabase.toml",
        #     "sqlite3": r"DataBase\sqlitedatabase.db",
        # }
        pass

    def _confirm_configuration(self):
        # Do you want to start processing?
        pass

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
