from datetime import datetime, timedelta
from ..queries import GET_AVERAGE_PRICES
from ..utils.helpers import get_all_child_slugs, get_port_codes
from ..utils.validators import is_valid_port_code

def get_average_prices(conn, origin, destination, date_from, date_to):
    try:
        rates = list()

        # get origin and destination codes if they are codes
        origin_codes = [origin] if is_valid_port_code(origin) else []
        destination_codes = [destination] if is_valid_port_code(destination) else []

        # if the origin is a slug
        if not is_valid_port_code(origin):
            origin_slugs = get_all_child_slugs(conn, origin)
            for slug in origin_slugs:
                origin_codes.extend(get_port_codes(conn, slug))

        # if the destination is a slug
        if not is_valid_port_code(destination):
            destination_slugs = get_all_child_slugs(conn, destination)
            for slug in destination_slugs:
                destination_codes.extend(get_port_codes(conn, slug))

        # fetch the prices
        with conn.cursor() as cursor:
            cursor.execute(GET_AVERAGE_PRICES, (origin_codes, destination_codes, date_from, date_to))
            results = cursor.fetchall()

        # generates all dates from `date_from` to the range difference between `date_to` and `date_from`
        all_dates = [(date_from + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((date_to - date_from).days + 1)]
        # key-value pair with date as key and object as value
        result_dict = {result[0].strftime('%Y-%m-%d'): result for result in results}

        for date in all_dates:
            # if date exists and average_price is not None (count >= 3)
            if date in result_dict and not (result_dict[date][1] is None):
                rates.append({"day": date, "average_price": int(result_dict[date][1])})
            else:
                rates.append({"day": date, "average_price": None})

        return rates
    except Exception as e:
        raise Exception(f"Database query error: {e}")