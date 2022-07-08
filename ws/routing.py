from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/sensor', consumers.SensorConsumer.as_asgi()),
    path('ws/plotter', consumers.PlotterConsumer.as_asgi())
]
