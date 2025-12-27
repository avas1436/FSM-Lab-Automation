import questionary  # type: ignore
from Director import LabResultManager  # type: ignore


class InteractiveLabResultManager:
    """Interactive CLI for extract and save LabResult"""

    """Interactive CLI for extract and save LabResult"""

    def _show_welcome(self):
        pass
        # "Lab Result Manager"
        # "Manage and save lab results",
        pass
        # "Lab Result Manager"
        # "Manage and save lab results",

    def _get_daily_file(self):
        # Step 1: Select Excel file
        pass
        # Step 1: Select Excel file
        pass

    def _get_date_range(self):
        # Step 2: Select day range
        # Step 2: Select day range

        # "Enter start day"
        # "Enter end day"
        # "Enter start day"
        # "Enter end day"

        # End day must be >= start day!
        # Re-enter end day
        pass
        # End day must be >= start day!
        # Re-enter end day
        pass

    def _get_extract_engine(self):
        # Step 3: Select extraction engine
        pass
        # Step 3: Select extraction engine
        pass

    def _get_saver_engine(self):
        # Step 4: Select saving format
        pass
        # Step 4: Select saving format
        pass

    def _get_output_path(self):
        # Step 5: Select output path
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
        # Processing completed successfully!

        # except Exception as e:
        #     Error during processing:

    # def run(self):
    #     try:
    #         while True:
    #             self._show_welcome()
    #             self._get_daily_file()
    #             self._get_date_range()
    #             self._get_extract_engine()
    #             self._get_saver_engine()
    #             self._get_output_path()
    # def run(self):
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
    # except KeyboardInterrupt:
    # Program interrupted by user.
    # except Exception as e:
    # Unexpected error:

    # Thank you for using Lab Result Manager!
    # Thank you for using Lab Result Manager!


if __name__ == "__main__":
    pass
    pass
