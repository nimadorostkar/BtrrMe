import os
import django
from django.core.asgi import get_asgi_application
from chat.middleware import JWTAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
print("Environment variable set")
django.setup()
print("Django setup complete")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
})
print("ASGI application loaded")
