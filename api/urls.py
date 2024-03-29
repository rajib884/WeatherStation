from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'
urlpatterns = [
    path('time', views.get_time, name='get_time'),
    path('token', obtain_auth_token, name='get_token'),
    path('check/token', views.check_token, name='check_token'),
    path('check/sensor_id', views.check_sensor_id, name='check_sensor_id'),
    path('user/', views.get_user, name='get_user'),
    path('sensors/', views.get_sensor, name='get_sensor'),
    path('sensors/<int:sensor_id>/', views.get_data, name='get_data'),
    path('sensors/add', views.add_data, name='add_data'),
]
