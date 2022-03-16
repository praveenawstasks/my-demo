from pyspark.sql import SparkSession, DataFrame
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logger.setLevel(logging.INFO)

class SparkClient:
    def __init__(self):
        self.spark = SparkSession.builder.appName("my-demo").getOrCreate()

    def read_csv(self, bucket: str, key: str, header: bool = True, delimiter: str = '|', infer_schema:bool = True):
        path = f"s3://{bucket}/{key}"
        logger.info(f"Reading file from bucket : {bucket} and key : {key} and path : {path}")
        return self.spark.read\
            .option("header", header)\
            .option("delimiter", delimiter) \
            .option("inferSchema", infer_schema) \
            .csv(path)

    def write_csv(self, df: DataFrame, bucket: str, key: str, header: bool = True, delimiter: str = '|'):
        path = f"s3://{bucket}/{key}"
        logger.info(f"Writing file to bucket : {bucket} and key : {key} and path : {path}")
        df.write.option("header", header).option("delimiter", delimiter).mode("overwrite").csv(path)

    def read_spark_temp_table(self, table_name: str):
        return self.spark.sql(f'SELECT * from {table_name}')

    def read_spark_query(self, query: str):
        return self.spark.sql(query)
