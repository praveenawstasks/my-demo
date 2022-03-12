#from spark_util import SparkClient

class Driver:
    def __init__(self):
        pass
        #self.spark_client = SparkClient()

    def execute_job(self):
        print('In execute job..')
        bucket = 'praveen-demo-bucket1'
        key = 'input/data.tsv'
        #df = self.spark_client.read_csv(bucket,key, delimiter='	')
        print('Printing dataframe..')
        #df.show()