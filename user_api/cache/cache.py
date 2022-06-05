import os
import json

import redis

from models.user import User

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')


class Cache:
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def save_cache(self, user_id: int, user: User):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return
        except Exception as e:
            return

        user_dict = user.dict()
        cacheable_user = json.dumps(user_dict)
        self.redis.set(user_id, cacheable_user)

    def get_cache(self, user_id: int):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return None
        except Exception as e:
            return None

        cached_user = self.redis.get(user_id)

        if cached_user is None:
            return None

        decoded_user = cached_user.decode("utf-8")
        return json.loads(decoded_user)

    def delete_cache(self, user_id: int):
        # Ignore cache if not connected!
        try:
            if not self.redis.ping():
                return
        except Exception as e:
            return

        self.redis.delete(user_id)
