from util.util import today_date

config = {
    'extract':  [{'prefix': 'revenue_data', 'file_type': 'csv', 'delimiter': '	'}],
    'transform': {'query' : """
                               SELECT user_agent, geo_city, geo_region FROM revenue_data
                            """,
                  'table_name': 'temp_revenue_data'
                 },
    'load': {'output_file_name': f"{today_date()}_SearchKeywordPerformance.tab",
             'delimiter': '	',
             'output_key': "output/results/"}
}