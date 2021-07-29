from .base import *


DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


ALLOWED_HOSTS = [
    "lookup.ay-bryson.com",
]


REDIS_HOSTNAME = "redis"
CELERY_BROKER_URL = f"redis://{REDIS_HOSTNAME}:6379"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOSTNAME}:6379"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOSTNAME, 6379)],
        },
    },
}
