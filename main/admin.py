from django.contrib import admin

from .models import DataPoint


class DataPointAdmin(admin.ModelAdmin):
    list_display = ('date', 'temperature', 'humidity', 'pressure')
    fields = ['date', 'temperature', 'humidity', 'pressure']


admin.site.register(DataPoint, DataPointAdmin)
