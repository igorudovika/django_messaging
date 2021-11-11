from django.urls import path

from .consumers import WSConsumer

ws_urlpatterns = [
    path('ws/messages-monitor', WSConsumer.as_asgi())
]