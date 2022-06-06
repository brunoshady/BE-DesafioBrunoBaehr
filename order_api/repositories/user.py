import os

import requests

from cache.cache import Cache

USER_API_URL = os.environ.get('USER_API_URL')


def get_user_by_id(user_id: int, mock_user: dict):
    try:
        # TODO - little workaround, precisaria remover um dia ^^
        if mock_user:
            return mock_user

        cached_user = Cache().get_user_cache(user_id)
        if cached_user:
            return cached_user

        url = f'{USER_API_URL}/{user_id}'
        response = requests.get(url)
        if response.status_code == 404:
            return None

        user_dict = response.json()
        Cache().save_user_cache(user_id, user_dict)
    except Exception as e:
        raise e

    return user_dict
