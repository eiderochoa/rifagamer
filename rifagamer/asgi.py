"""
ASGI config for rifagamer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from dashboard.consumers import WSConsumer
from django.conf import settings
from django.conf.urls.static import static
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rifagamer.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter([
        path('ws/percent', WSConsumer.as_asgi())
        ]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)))
})

