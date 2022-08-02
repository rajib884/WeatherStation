from django.contrib import admin

from .models import DataPoint, Sensor


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    fields = ['name', 'owner']


class DataPointAdmin(admin.ModelAdmin):
    pass
    # list_display = ('date', 'temperature', 'humidity', 'pressure')
    # fields = ['date', 'temperature', 'humidity', 'pressure']


admin.site.register(Sensor, SensorAdmin)
admin.site.register(DataPoint, DataPointAdmin)
