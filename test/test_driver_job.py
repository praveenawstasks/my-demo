import unittest
from datetime import date
from mock import patch
from driver_job import Driver
import os

@patch.dict('driver_job.module_map', {
    'test_key': 'test_module'
})
@patch('driver_job.EtlProcess')
@patch('driver_job.SparkClient')
class DriverJobTest(unittest.TestCase):
    def test_driver_job(self, mock_etl, mock_spark):
        driver_obj = Driver('test_bucket', 'input/test_key.csv')
        driver_obj.execute_job()
        assert driver_obj.config == {'test_config_key': 'test_config_value', 'domain': 'test_module'}
        assert driver_obj.domain == 'test_module'


if __name__ == '__main__':
    unittest.main()