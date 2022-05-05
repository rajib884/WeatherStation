from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import serializers
from main.models import Sensor, DataPoint


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    # datapoint = serializers.PrimaryKeyRelatedField(many=True, queryset=DataPoint.objects.all())
    # datapoint = DataPointSerializer(many=True, read_only=True)
    datapoint = serializers.SerializerMethodField()

    @staticmethod
    def get_datapoint(sensor):
        query = DataPoint.objects.filter(sensor=sensor).order_by('date').last()
        serializer = DataPointSerializer(query, many=False)
        return serializer.data

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'datapoint']


class UserSerializer(serializers.ModelSerializer):
    # tokens = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # sensors = serializers.StringRelatedField(many=True)
    # sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'sensors']
