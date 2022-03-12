import argparse

from pyspark.sql import SparkSession


def calculate_red_violations():
    """
    Processes sample food establishment inspection data and queries the data to find the top 10 establishments
    with the most Red violations from 2006 to 2020.

    :param data_source: The URI of your food establishment data CSV, such as 's3://DOC-EXAMPLE-BUCKET/food-establishment-data.csv'.
    :param output_uri: The URI where output is written, such as 's3://DOC-EXAMPLE-BUCKET/restaurant_violation_results'.
    """
    with SparkSession.builder.appName("Calculate Red Health Violations").getOrCreate() as spark:
        # Load the restaurant violation CSV data
        data_source = "s3://praveen-demo-bucket1/input/food_establishment_data.csv"
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
        output_uri = "s3://praveen-demo-bucket1/input/"
        top_red_violation_restaurants.write.option("header", "true").mode("overwrite").csv(output_uri)
        print('Process completed...')

if __name__ == "__main__":
    print('Process started...')
    calculate_red_violations()
