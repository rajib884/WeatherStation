from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='about'),  # future
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sensor/<int:sensor_num>', views.sensor, name='sensor'),
    path('sensor/<int:sensor_num>/download', views.get_sensor_data, name='get_sensor_data'),
]
