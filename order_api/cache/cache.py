import os
import json

import redis

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')


class Cache:
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def save_order_cache(self, order_id: int, order_dict: dict):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return
        except Exception as e:
            return

        key_dict = json.dumps({'order_id': order_id})
        cacheable_order = json.dumps(order_dict)
        self.redis.set(key_dict, cacheable_order)

    def get_order_cache(self, order_id: int):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return None
        except Exception as e:
            return None

        key_dict = json.dumps({'order_id': order_id})
        cached_order = self.redis.get(key_dict)

        if cached_order is None:
            return None

        decoded_order = cached_order.decode("utf-8")
        return json.loads(decoded_order)

    def delete_order_cache(self, order_id: int):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return
        except Exception as e:
            return

        key_dict = json.dumps({'order_id': order_id})
        self.redis.delete(key_dict)

    def save_user_cache(self, user_id: int, user_dict: dict):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return
        except Exception as e:
            return

        key_dict = json.dumps({'user_id': user_id})
        cacheable_user = json.dumps(user_dict)
        self.redis.set(key_dict, cacheable_user)

    def get_user_cache(self, user_id: int):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return None
        except Exception as e:
            return None

        key_dict = json.dumps({'user_id': user_id})
        cached_user = self.redis.get(key_dict)

        if cached_user is None:
            return None

        decoded_user = cached_user.decode("utf-8")
        return json.loads(decoded_user)
