from util.spark_util import SparkClient
import importlib.util
import argparse
from etl_process import EtlProcess
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logger.setLevel(logging.INFO)

module_map = {
    'revenue_data': 'revenue'
}

class Driver:
    def __init__(self, source_bucket, source_key):
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.spark_client = SparkClient()
        self.domain = None

    def get_module(self):
        job_identifier = self.source_key.split('.')[0].split('/')[1]
        logger.info(f"Fetching module {job_identifier}...")
        module_name = module_map[job_identifier]
        self.domain = module_name
        module_spec = importlib.util.find_spec(f"config.{module_name}")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def execute_job(self):
        logger.info('Execute job..')
        module = self.get_module()
        config = module.config
        config['domain'] = self.domain
        logger.info(f"Etl configuration : {config}")
        etl_obj = EtlProcess(self.source_bucket, self.source_key, config, self.spark_client)
        etl_obj.do_etl_process()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_key')
    parser.add_argument(
        '--source_bucket')
    args = parser.parse_args()
    logger.info(f'Parsed arguments : {args}')

    driver = Driver(args.source_bucket, args.source_key)
    driver.execute_job()