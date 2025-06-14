import polars as pl
import sys
import re

sys.path.append("..")
from configs.data_configs import PROCESSED_DATA_DIR, RAW_FILE_LIST

from tqdm.auto import tqdm
import os
import glob


class DataPreprocessing:
    def __init__(self, data_ingestor, nyc, total_batches):
        self.data_ingestor = data_ingestor
        self.nyc = nyc
        self.total_batches = total_batches

    @staticmethod
    def preprocess_batch(data: pl.DataFrame):
        """
        Apply necessary preprocessing steps: removing unwanted columns, transforming, etc.
        """
        # Add 'dropoff_date' and 'dropoff_month' columns
        data = data.with_columns(
            [
                data["dropoff_datetime"].dt.date().alias("dropoff_date"),
                data["dropoff_datetime"].dt.month().alias("dropoff_month"),
            ]
        )

        # Remove unwanted columns
        unwanted_columns = [
            "pickup_datetime",
            "dropoff_datetime",
            "request_datetime",
            "on_scene_datetime",
            "hvfhs_license_num",
            "airport_fee",
            "dispatching_base_num",
            "shared_request_flag",
            "originating_base_num",
            "shared_match_flag",
            "access_a_ride_flag",
            "wav_request_flag",
            "wav_match_flag",
        ]
        data = data.drop(unwanted_columns)

        return data

    def clean_processed_data_dir(self):
        """
        Clean the PROCESSED_DATA_DIR by removing old .parquet files.
        """
        try:
            # Clean up existing Parquet files in the processed data directory
            files = glob.glob(f"{PROCESSED_DATA_DIR}/*.parquet")
            for f in files:
                os.remove(f)

            # Ensure the processed data directory exists, if not, create it
            os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

        except FileNotFoundError:
            print(
                f"Processed Data Directory not found, creating directory: {PROCESSED_DATA_DIR}"
            )
            try:
                os.makedirs(PROCESSED_DATA_DIR)
            except Exception as e:
                print(f"Error creating Processed Data Directory: {e}")
                raise e  # Raising to handle it outside if needed
        except Exception as e:
            print(f"Error cleaning Processed Data Directory: {e}")
            raise e  # Raising to handle it outside if needed

    def preprocess_data(self):
        """
        Main function to process the data through batches.
        """
        try:
            # Clean and prepare the processed data directory
            self.clean_processed_data_dir()

            for file_path in tqdm(RAW_FILE_LIST, desc="Processing Files", unit="file"):
                data = pl.read_parquet(file_path)
                data = self.preprocess_batch(data)
                data = data.join(
                    self.nyc, left_on="dropoff_date", right_on="datetime", how="inner"
                ).drop("dropoff_date")

                match = re.search(r"(\d{4}-\d{2})", file_path)
                if match:
                    year_month = match.group(1)
                    out_file_name = (
                        f"{PROCESSED_DATA_DIR}/tripdata_{year_month}.parquet"
                    )
                    data.write_parquet(out_file_name)
            print("Data Processing Completed!")

        except Exception as e:
            print(f"Data Processing Failed! Error: {e}")
            sys.exit(1)
