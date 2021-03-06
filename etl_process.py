from util.spark_util import SparkClient
import logging
import sys
import glob
import shutil
import boto3

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logger.setLevel(logging.INFO)

class EtlProcess:
    def __init__(self, source_bucket:str, source_key:str, config: dict, spark_client: SparkClient):
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.config = config
        self.spark_client = spark_client
        self.domain = self.config['domain']

    def do_etl_process(self):
        self.extract()
        temp_table_name = self.transform()
        self.load(temp_table_name)

    def extract(self):
        logger.info('In Extraction step...')
        logger.info(f'Processing ETL for domain : {self.domain}...')
        extract_config = self.config['extract']
        for conf in extract_config:
            if conf['prefix'] in self.source_key:
                table_name = conf['prefix']
                file_type = conf['file_type']
                if file_type == 'csv':
                    delimiter = conf['delimiter']
                    logger.info(f"Extracting data from bucket : {self.source_bucket} and key : {self.source_key}")
                    df = self.spark_client.read_csv(self.source_bucket, self.source_key, delimiter = delimiter)
                    df.createOrReplaceTempView(table_name)
                    logger.info(f"Created temp table : {table_name}")

    def transform(self):
        logger.info('In Transformation step...')
        temp_table_name = ""
        transform_config = self.config['transform']
        for config in transform_config:
            query = config['query']
            temp_table_name = config['table_name']
            self.spark_client.read_spark_query(query).createOrReplaceTempView(temp_table_name)
            logger.info(f"Transforming data from temp table : {temp_table_name} using below query...")
            logger.info(query)
        return temp_table_name


    def load(self, temp_table_name):
        logger.info('In Load step...')
        load_config = self.config['load']
        delimiter = load_config['delimiter']
        temp_path = f'temp/{self.domain}/'
        df = self.spark_client.read_spark_temp_table(temp_table_name)
        logger.info(f"Writing dataframe into bucket : {self.source_bucket} and path : {temp_path}")
        self.spark_client.write_csv(df, self.source_bucket, temp_path, delimiter= delimiter, coalesce_count=1)
        self.spark_client.read_spark_temp_table(temp_table_name).show()
        self.copy_file_to_path(temp_path)

    def copy_file_to_path(self, source_path):
        logger.info("Writing as tab file for output...")
        load_config = self.config['load']
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.source_bucket)
        prefix_objs = bucket.objects.filter(Prefix=source_path)
        csv_path = [obj.key for obj in prefix_objs if obj.key[-4:] == '.csv'][0]
        logger.info(f"Generated temp csv : {csv_path}")
        copy_source = {
            'Bucket' : self.source_bucket,
            'Key': csv_path
        }
        output_path = f"{load_config['output_key_prefix']}{self.domain}"
        output_file_name = load_config['output_file_name']
        output_key = f"{output_path}/{output_file_name}"
        s3.meta.client.copy(copy_source, self.source_bucket, output_key)
        logger.info(f'Written final output file in bucket: {self.source_bucket}  and key : {output_key}')

