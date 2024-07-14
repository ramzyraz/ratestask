GET_PORT_CODES = """
    SELECT code 
    FROM ports 
    WHERE parent_slug = %s
"""

GET_CHILD_SLUGS = """
    SELECT slug 
    FROM regions 
    WHERE parent_slug = %s
"""

GET_AVERAGE_PRICES = """
    SELECT day, 
        CASE 
            WHEN COUNT(*) >= 3 THEN CAST(ROUND(AVG(price)) AS INTEGER)
            ELSE NULL
        END as average_price
    FROM prices
    WHERE orig_code = ANY(%s) AND dest_code = ANY(%s)
        AND day BETWEEN %s AND %s
    GROUP BY day
    ORDER BY day
"""