"""
ASGI config for communication_portal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from .routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communication_portal.settings')

application = ProtocolTypeRouter({'http': get_asgi_application(),
                                   'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
                                   })
