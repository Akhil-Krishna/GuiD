import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from main.routing import websocket_urlpatterns as main_websocket_urlpatterns
from forum.routing import websocket_urlpatterns as forum_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guid.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main_websocket_urlpatterns + forum_websocket_urlpatterns
        )
    ),
})
