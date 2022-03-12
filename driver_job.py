from util.spark_util import SparkClient
import importlib.util
import argparse
from etl_process import EtlProcess

module_map = {
    'revenue_data': 'revenue'
}


class Driver:
    def __init__(self, source_bucket, source_key):
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.spark_client = SparkClient()

    def get_module(self):
        print(f"Fetching module {self.source_key.split('.')[0]}...")
        module_name = module_map[self.source_key.split('.')[0]]
        module_spec = importlib.util.find_spec(f"config.{module_name}")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def execute_job(self):
        print('In execute job..')
        module = self.get_module()
        print(module.config)
        etl_obj = EtlProcess(self.source_bucket, self.source_key, module.config, self.spark_client)
        etl_obj.do_etl_process()
        bucket = 'praveen-demo-bucket1'
        key = 'input/revenue_data.tsv'
        df = self.spark_client.read_csv(bucket,key, delimiter='	')
        print('Printing dataframe..')
        df.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_key')
    parser.add_argument(
        '--source_bucket')
    args = parser.parse_args()
    print(f'Parsed arguments : {args}')

    driver = Driver(args.source_bucket, args.source_key)
    driver.execute_job()