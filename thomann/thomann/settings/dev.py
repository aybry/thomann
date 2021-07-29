from .base import *


DEBUG = True


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


REDIS_HOSTNAME = "127.0.0.1"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOSTNAME, 6379)],
        },
    },
}
