
from django.urls import path
from api.market.consumers import MarketConsumers
websocket_urlpatterns = [
    path(r'ws/market/', MarketConsumers.as_asgi())
]