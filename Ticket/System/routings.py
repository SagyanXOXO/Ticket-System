from django.urls import path
from . import consumers

"""

urlpatterns for websocket

"""
websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]