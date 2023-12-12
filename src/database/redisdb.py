"""redis db"""
import datetime
import json

import redis

from src.settings import REDIS_URL, TIME_EXPIRE


r = redis.Redis(host=REDIS_URL.split(":")[0], port=REDIS_URL.split(":")[1], decode_responses=True)


class MyRedisCli:
    """Redis CRUD"""

    @staticmethod
    async def insert_data(key: str, **kwargs) -> bool:
        """create data"""
        res = r.set(
            name=key,
            value=json.dumps(kwargs),
            ex=datetime.timedelta(minutes=TIME_EXPIRE)
        )
        return res

    @staticmethod
    async def update_data(key: str, **kwargs):
        """update data"""
        data = r.get(name=key)
        if data:
            old_data = json.loads(data)
            new_data = old_data | kwargs
            res = r.set(
                name=key,
                value=json.dumps(new_data),
                ex=datetime.timedelta(minutes=TIME_EXPIRE)
            )
            return res
        return None

    @staticmethod
    async def get_data(key: str):
        """read data"""
        res = r.get(key)
        if res:
            return json.loads(res)
        return None

    @staticmethod
    async def delete_data(key: str):
        """delete data"""
        res = r.delete(key)
        return res
