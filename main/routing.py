from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/code/', consumers.CodeConsumer.as_asgi()),
]
