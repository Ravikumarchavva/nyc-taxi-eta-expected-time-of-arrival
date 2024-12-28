import polars as pl
import sys

sys.path.append("..")

from components.data_ingestion import DataIngestion
from components.data_preprocessing import DataPreprocessing
from components.feature_engineering import FeatureEngineering

# Large Dataset
file_list = [
    "../data/fhvhv_tripdata_2021-01.parquet",
    "../data/fhvhv_tripdata_2021-02.parquet",
    "../data/fhvhv_tripdata_2021-03.parquet",
    "../data/fhvhv_tripdata_2021-04.parquet",
    "../data/fhvhv_tripdata_2021-05.parquet",
    "../data/fhvhv_tripdata_2021-06.parquet",
    "../data/fhvhv_tripdata_2021-07.parquet",
    "../data/fhvhv_tripdata_2021-08.parquet",
    "../data/fhvhv_tripdata_2021-09.parquet",
    "../data/fhvhv_tripdata_2021-10.parquet",
    "../data/fhvhv_tripdata_2021-11.parquet",
    "../data/fhvhv_tripdata_2021-12.parquet",
]

# Create an instance of the DataIngestion class
data_ingestor = DataIngestion(file_list, batch_size=5_000_000)