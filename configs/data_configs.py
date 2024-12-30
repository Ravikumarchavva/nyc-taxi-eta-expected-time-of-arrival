import os
from pathlib import Path

# Define the directories
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / 'data'
RAW_DATA_DIR_SMALL = DATA_DIR / 'rawdata'
RAW_DATA_DIR = DATA_DIR / 'raw_data'
PROCESSED_DATA_DIR = DATA_DIR / 'processed_data'
MODEL_DATA_DIR = DATA_DIR / 'model_data'

# Helper function to get sorted .parquet files
def get_parquet_files(dir_path):
    return sorted([os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.endswith('.parquet')])

# Get the lists of .parquet files
RAW_FILE_LIST = get_parquet_files(RAW_DATA_DIR)
PROCESSED_FILE_LIST = get_parquet_files(PROCESSED_DATA_DIR)


if __name__ == '__main__':
    print(RAW_FILE_LIST)
    print(PROCESSED_FILE_LIST)