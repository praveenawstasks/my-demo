from util.util import today_date

config = {
    'extract':  [{'prefix': 'revenue_data', 'file_type': 'csv', 'delimiter': '	'}],
    'transform': [
        {'query': """
                   select hit_time_gmt, event_list, pagename, page_url,
                   coalesce(pagename, case when trim(page_url) = 'https://www.esshopzilla.com/checkout/?a=complete' then 'Order Complete' else 'Purchase Error' end) as purchase_status,
                   product_list, referrer,
                   concat(split(split(split(referrer, '//')[1], '/')[0], '[\.]')[1], '\.', split(split(split(referrer, '//')[1], '/')[0], '[\.]')[2]) as external_search_engine,
                   split(product_list, ',') as products
                   from revenue_data
                   where event_list = 1
                  """,
         'table_name': 'temp_hit_data'
        },
        {'query': """
                   select purchase_status,
                   external_search_engine,
                   split(product_info, ';')[0] as category,
                   split(product_info, ';')[1] as product,
                   split(product_info, ';')[2] as units,
                   split(product_info, ';')[3] as cost,
                   product_info                   
                   from 
                   (
                       select purchase_status, 
                       external_search_engine,
                       explode(split(product_list, ',')) as product_info 
                       from temp_hit_data
                   ) a
                  """,
         'table_name': 'product_data'
        },
        {'query': """
                   select 
                   external_search_engine, 
                   product, 
                   sum(cost) as total_cost 
                   from product_data
                   group by 
                   external_search_engine,
                   product
                   order by sum(cost) desc
                  """,
         'table_name': 'final_data'
        },
    ],
    'load': {'output_file_name': f"{today_date()}_SearchKeywordPerformance.tab",
             'delimiter': '	',
             'output_key_prefix': "output/"}
}