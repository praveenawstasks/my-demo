

config = {
    'extract':  [{'prefix': 'revenue_data', 'file_type': 'csv', 'delimiter': '	'}],
    'transform': {'query' : """
                               SELECT user_agent, geo_city, geo_region FROM revenue_data
                            """,
                  'table_name': 'temp_revenue_data'
                 },
    'load': {}
}