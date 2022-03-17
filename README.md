# my-demo

This project generates the revenue for different products searched through online search engines.

Command to run the job:
spark-submit driver_job.py --source_key input/revenue_data.tsv --source_bucket praveen-demo-bucket1

or

spark-submit driver_job.py --source_key input/revenue_data.tsv 


if source_bucket is skipped from the command, default bucket considered is praveen-demo-bucket1