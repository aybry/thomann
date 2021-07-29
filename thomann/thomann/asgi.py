import os

from django.core.asgi import get_asgi_application
from django.urls import path
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from lookup_hub.consumers import row, category


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thomann.settings.dev")

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/row/<str:dict_slug>", row.RowConsumer.as_asgi()),
            path("ws/category/<str:dict_slug>", category.CategoryConsumer.as_asgi()),
        ])
    ),
})
