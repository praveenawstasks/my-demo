import argparse
import sys
from pyspark.sql import SparkSession
import os

def calculate_red_violations():
    """
    Processes sample food establishment inspection data and queries the data to find the top 10 establishments
    with the most Red violations from 2006 to 2020.

    :param data_source: The URI of your food establishment data CSV, such as 's3://DOC-EXAMPLE-BUCKET/food-establishment-data.csv'.
    :param output_uri: The URI where output is written, such as 's3://DOC-EXAMPLE-BUCKET/restaurant_violation_results'.
    """
    # print(sys.argv)
    # print(os.environ['PATH'])
    # SPARK_HOME = r"C:\Users\mysecondstep\mypythonenvironments\pyspark\spark-3.2.1-bin-hadoop3.2"
    # os.environ['SPARK_HOME'] = SPARK_HOME
    # os.environ['PYTHONPATH'] = f"{SPARK_HOME}\python\;{SPARK_HOME}\python\lib\py4j-0.10.9.3-src.zip;{SPARK_HOME}\python\lib\pyspark.zip"
    # os.environ['JAVA_HOME'] = r"C:\Users\mysecondstep\mypythonenvironments\openjdk-17.0.2_windows-x64_bin\jdk-17.0.2"
    # #os.environ['JAVA_HOME'] = "C:\Program Files\Java\jdk1.8.0_161"
    # os.environ['PATH'] = r"C:\Users\mysecondstep\mypythonenvironments\pyspark\spark-3.2.1-bin-hadoop3.2\bin;" + r"C:\Users\mysecondstep\mypythonenvironments\openjdk-17.0.2_windows-x64_bin\jdk-17.0.2\bin"
    # print(os.environ['PYTHONPATH'])
    # print(os.environ['PATH'])
    # os.environ['PYSPARK_SUBMIT_ARGS'] = "--master local[*] pyspark-shell"

    SPARK_HOME = r"C:\Users\mysecondstep\mypythonenvironments\pyspark\spark-3.2.1-bin-hadoop3.2"
    PATH = r"C:\Users\mysecondstep\mypythonenvironments\pyspark\spark-3.2.1-bin-hadoop3.2\bin"
    PYTHONPATH = f"{SPARK_HOME}\python:{SPARK_HOME}\python\lib\py4j-0.10.9.3-src.zip"
    JAVA_PATH = r"C:\Users\mysecondstep\mypythonenvironments\openjdk-17.0.2_windows-x64_bin\jdk-17.0.2"
    FINAL_PATH = f"{JAVA_PATH}\bin:{SPARK_HOME}\python:{PATH}"

    os.environ['SPARK_HOME'] = SPARK_HOME
    os.environ['PYTHONPATH'] = PYTHONPATH
    os.environ['PATH'] = FINAL_PATH
    os.environ['JAVA_HOME'] = r"C:\Users\mysecondstep\mypythonenvironments\openjdk-17.0.2_windows-x64_bin\jdk-17.0.2"
    os.environ['PYSPARK_SUBMIT_ARGS'] = "--master local[*] pyspark-shell"

    with SparkSession.builder.appName("Calculate Red Health Violations").getOrCreate() as spark:
        # Load the restaurant violation CSV data
        data_source = "food_establishment_data.csv"
        print(data_source)
        print(f'Reading data from {data_source}')
        restaurants_df = spark.read.option("header", "true").csv(data_source)
        restaurants_df.show(5)

        # Create an in-memory DataFrame to query
        restaurants_df.createOrReplaceTempView("restaurant_violations")

        # Create a DataFrame of the top 10 restaurants with the most Red violations
        top_red_violation_restaurants = spark.sql("""SELECT name, count(*) AS total_red_violations 
          FROM restaurant_violations 
          WHERE violation_type = 'RED' 
          GROUP BY name 
          ORDER BY total_red_violations DESC LIMIT 10""")

        print('Output DF...')
        top_red_violation_restaurants.show(4)

        # Write the results to the specified output URI
        output_uri = "output/result"
        top_red_violation_restaurants.write.option("header", "true").mode("overwrite").csv(output_uri)
        print('Process completed...')

if __name__ == "__main__":
    print('Process started...')
    calculate_red_violations()
