import os
import requests

ORDER_API_URL = os.environ.get('ORDER_API_URL')


def get_orders_by_user(user_id: int):
    try:
        url = f'{ORDER_API_URL}{user_id}'
        response = requests.get(url)
        if response.status_code == 404:
            return None

        orders = response.json()
    except Exception as e:
        raise e

    return orders
