import polars as pl
import sys

sys.path.append("..")
from nyc_taxi_eta_expected_time_of_arrival.utils.data_utils import Preprocess
from tqdm.auto import tqdm


class DataIngestion:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.current_file_index = 0
        self.current_df = None

    def _load_next_file(self):
        """
        Load the next file in the list.
        """
        if self.current_file_index >= len(self.file_paths):
            raise StopIteration

        file_path = self.file_paths[self.current_file_index]
        # Load the DataFrame and apply preprocessing
        self.current_df = pl.read_parquet(file_path).pipe(
            lambda df: Preprocess.reduce_memory_usage(df, print_info=False)
        )
        self.current_file_index += 1

    def __iter__(self):
        return self

    def __next__(self):
        """
        Yield the next file as a whole DataFrame.
        """
        if self.current_df is None:
            self._load_next_file()

        # Return the current file's DataFrame and prepare for the next file
        data_to_return = self.current_df
        self.current_df = None  # Reset so the next file is loaded

        return data_to_return

    # Define a method to get the total number of rows and files in the dataset
    def get_dataset_stats(self):
        total_rows = 0
        total_files = len(self.file_paths)

        for file_path in tqdm(
            self.file_paths, desc="Calculating total rows", unit="file"
        ):
            df = pl.read_parquet(file_path)
            total_rows += df.height

        return f"{total_rows:_}", total_files

    # Define the __len__ method to return the total number of rows in all files
    def __len__(self):
        total_rows = 0

        for file_path in tqdm(
            self.file_paths, desc="Calculating total rows", unit="file"
        ):
            df = pl.read_parquet(file_path)
            total_rows += df.height

        return f"{total_rows:_}"
