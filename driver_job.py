from util.spark_util import SparkClient
import importlib.util
import argparse

module_map = {
    'revenue_data': 'revenue'
}


class Driver:
    def __init__(self, source_file):
        self.source_file = source_file
        self.spark_client = SparkClient()

    def get_module(self):
        print(f"Fetching module {self.source_file.split('.')[0]}...")
        module_name = module_map[self.source_file.split('.')[0]]
        module_spec = importlib.util.find_spec(f"config/{module_name}")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def execute_job(self):
        print('In execute job..')
        module = self.get_module()
        print(module.config)
        bucket = 'praveen-demo-bucket1'
        key = 'input/revenue_data.tsv'
        df = self.spark_client.read_csv(bucket,key, delimiter='	')
        print('Printing dataframe..')
        df.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_file')
    args = parser.parse_args()
    print(f'Parsed arguments : {args}')

    driver = Driver(args.source_file)
    driver.execute_job()