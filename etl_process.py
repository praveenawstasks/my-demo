from util.spark_util import SparkClient
class EtlProcess:
    def __init__(self, source_bucket:str, source_key:str, config: dict, spark_client: SparkClient):
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.config = config
        self.spark_client = spark_client

    def do_etl_process(self):
        self.extract()
        self.transform()
        self.load()

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
        df.show()

    def transform(self):
        pass

    def load(self):
        pass