import os

BATCH_SIZE = 5_000_000

# Get absolute directory paths
RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data'))
PROCESSED_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed_data'))

# Helper function to get sorted .parquet files
def get_parquet_files(dir_path):
    return sorted([os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.endswith('.parquet')])

# Get the lists of .parquet files
RAW_FILE_LIST = get_parquet_files(RAW_DATA_DIR)
PROCESSED_FILE_LIST = get_parquet_files(PROCESSED_DATA_DIR)

if __name__ == '__main__':
    print(RAW_DATA_DIR)
    print(PROCESSED_DATA_DIR)
    print(RAW_FILE_LIST)
    print(PROCESSED_FILE_LIST)
