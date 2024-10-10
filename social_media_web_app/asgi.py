"""
ASGI config for social_media_web_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing
from django.conf import settings

# settings.configure()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_web_app.settings')

# print(os.environ.get('DJANGO_SETTINGS_MODULE'), " value")



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # WebSocket routes go here
        )
    ),
})
