"""
ASGI config for Settings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from Something.routing import channels_routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
      AuthMiddlewareStack(URLRouter(channels_routing))  
    )
})
