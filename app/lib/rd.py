import redis
import os

host = os.getenv('REDIS_HOST')
password = os.getenv('REDIS_PASSWORD')

r = redis.Redis(
    host=host,
    port=10918,
    decode_responses=True,
    username="default",
    password=password,
)