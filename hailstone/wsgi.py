"""
WSGI config for hailstone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.wsgi import get_wsgi_application
import api.routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hailstone.settings')

application = ProtocolTypeRouter({
    'http':  get_wsgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.routings.websocket_urlpatterns
        )
    ),
})