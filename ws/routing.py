from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/sensor', consumers.SensorConsumer.as_asgi()),
    path('ws/plotter/<int:sensor_num>', consumers.PlotterConsumer.as_asgi())
]
