from pyspark.sql import SparkSession, DataFrame

class SparkClient:
    def __init__(self):
        self.spark = SparkSession.builder.appName("my-demo").getOrCreate()

    def read_csv(self, bucket: str, key: str, header: bool = True, delimiter: str = '|'):
        path = f"s3://{bucket}/{key}"
        print(f"Reading file from bucket : {bucket} and key : {key} and path : {path}")
        return self.spark.read.option("header", header).option("delimiter", delimiter).csv(path)

    def write_csv(self, df: DataFrame, bucket: str, key: str, header: bool = True, delimiter: str = '|'):
        path = f"s3://{bucket}/{key}"
        print(f"Writing file to bucket : {bucket} and key : {key} and path : {path}")
        df.write.option("header", header).option("delimiter", delimiter).mode("overwrite").csv(path)

    def read_spark_temp_table(self, table_name: str):
        return self.spark.sql(f'SELECT * from {table_name}')

    def read_spark_query(self, query: str):
        return self.spark.sql(query)
