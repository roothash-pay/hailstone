"""
ASGI config for server project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import api.routings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hailstone.settings')

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            api.routings.websocket_urlpatterns
        )
    ),
    "http": get_asgi_application(),
})
