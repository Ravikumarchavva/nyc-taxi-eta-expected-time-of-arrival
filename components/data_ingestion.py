import polars as pl
import sys
sys.path.append("..")
from utils.data_utils import Preprocess
from tqdm.auto import tqdm

class DataIngestion:
    def __init__(self, file_paths, batch_size=5_000_000):
        self.file_paths = file_paths
        self.batch_size = batch_size
        self.current_file_index = 0
        self.current_df = None
        self.current_offset = 0

    def _load_next_file(self):
        """
        Load the next file in the list.
        """
        if self.current_file_index >= len(self.file_paths):
            raise StopIteration
        
        file_path = self.file_paths[self.current_file_index]
        self.current_df = pl.read_parquet(file_path).pipe(lambda df: Preprocess.reduce_memory_usage(df, print_info=False))
        self.current_offset = 0
        self.current_file_index += 1

    def __iter__(self):
        return self
    

    def __next__(self):
        """
        Yield a batch from the current file.
        """
        if self.current_df is None or self.current_offset >= self.current_df.height:
            self._load_next_file()

        # Define the end of the current batch
        end_offset = min(self.current_offset + self.batch_size, self.current_df.height)
        
        # Slice the DataFrame for the current batch
        batch = self.current_df.slice(self.current_offset, end_offset - self.current_offset)
        self.current_offset = end_offset
        return batch
    
    # Define a method to get the total number of rows and batches in the dataset
    def get_dataset_stats(self):
        total_rows = 0
        total_batches = 0
        
        for file_path in tqdm(self.file_paths, desc="Calculating total rows & batches", unit="file"):
            df = pl.read_parquet(file_path)
            file_rows = df.height
            total_rows += file_rows
            total_batches += (file_rows + self.batch_size - 1) // self.batch_size  # Ceiling division

        return f"{total_rows:_}", total_batches


    # Define the __len__ method to calculate batch count
    def __len__(self):
        total_rows = 0
        
        for file_path in tqdm(self.file_paths, desc="Calculating total rows & batches", unit="file"):
            df = pl.read_parquet(file_path)
            file_rows = df.height
            total_rows += file_rows

        return f"{total_rows:_}"
