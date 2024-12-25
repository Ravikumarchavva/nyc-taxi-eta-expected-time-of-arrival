# Convert to spark
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, FloatType


class Preprocess:
    @staticmethod
    def calculate_memory_usage(data: DataFrame):
        return data.rdd.map(lambda x: x.memory_usage()).sum()
    
    @staticmethod
    def reduce_memory_usage(data: DataFrame):
        print(f"Memory usage before: {Preprocess.calculate_memory_usage(data):.2f} bytes")
        for column in data.columns:
            if data.schema[column].dataType == IntegerType():
                data = data.withColumn(column, col(column).cast("int"))
            elif data.schema[column].dataType == FloatType():
                data = data.withColumn(column, col(column).cast("float"))
        print(f"Memory usage after: {Preprocess.calculate_memory_usage(data):.2f} bytes")
        return data
    
# Change to use the IP address directly
# SPARK_MASTER_URL = "spark://192.168.245.142:7077"
SPARK_MASTER_URL = "local[*]"  # This runs Spark locally


SPARK_APP_NAME = 'Preprocess'

SPARK_CONFIG = {
    'spark.app.name': SPARK_APP_NAME,
    'spark.master': SPARK_MASTER_URL,
    'spark.executor.memory': '4g',
    'spark.executor.cores': '3',
}
    
# Create a Spark session with SLF4J library and other configurations
builder = SparkSession.builder
for key, value in SPARK_CONFIG.items():
    builder = builder.config(key, value)
spark = builder.getOrCreate()

data_2021_01 = spark.read.parquet("file:///mnt/d/github/uber-time-estimation/data/fhvhv_tripdata_2021-01.parquet")
data_2021_01 = Preprocess.reduce_memory_usage(data_2021_01)
data_2021_01.show(5)