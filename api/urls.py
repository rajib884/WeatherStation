from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.get_user, name='get_user'),
    path('sensors/', views.get_sensor, name='get_sensor'),
    path('sensors/<int:sensor_id>/', views.get_data, name='get_data'),
    path('sensors/add', views.add_data, name='add_data'),
]
