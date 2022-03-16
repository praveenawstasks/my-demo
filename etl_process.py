from util.spark_util import SparkClient
class EtlProcess:
    def __init__(self, source_bucket:str, source_key:str, config: dict, spark_client: SparkClient):
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.config = config
        self.spark_client = spark_client

    def do_etl_process(self):
        self.extract()
        temp_table_name = self.transform()
        self.load(temp_table_name)

    def extract(self):
        extract_config = self.config['extract']
        for conf in extract_config:
            if conf['prefix'] in self.source_key:
                table_name = conf['prefix']
                file_type = conf['file_type']
                if file_type == 'csv':
                    delimiter = conf['delimiter']
                    df = self.spark_client.read_csv(self.source_bucket, self.source_key, delimiter = delimiter)
                    df.createOrReplaceTempView(table_name)

    def transform(self):
        temp_table_name = ""
        transform_config = self.config['transform']
        for config in transform_config:
            query = config['query']
            temp_table_name = config['table_name']
            self.spark_client.read_spark_query(query).createOrReplaceTempView(temp_table_name)
        return temp_table_name


    def load(self, temp_table_name):
        load_config = self.config['load']
        output_file_name = load_config['output_file_name']
        delimiter = load_config['delimiter']
        output_key = f"{load_config['output_key']}{output_file_name}"
        df = self.spark_client.read_spark_temp_table(temp_table_name)
        self.spark_client.write_csv(df, self.source_bucket, output_key, delimiter= delimiter)
        self.spark_client.read_spark_temp_table(temp_table_name).show()
        import glob
        import shutil
        temp_file_name = glob.golb('output' + "/*.csv")[0]
        output_file_path = shutil.copy2(temp_file_name, output_key)
        #pd.to_csv(f"s3://{self.source_bucket}/output/output_file_name", delimiter=delimiter)

