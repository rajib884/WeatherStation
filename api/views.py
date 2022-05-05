from pprint import pprint

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import SensorSerializer, DataPointSerializer, UserSerializer
from main.models import Sensor, DataPoint


@api_view(['GET'])
def get_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_sensor(request):
    if request.user.is_authenticated:
        items = Sensor.objects.filter(owner=request.user)
        serializer = SensorSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_data(request, sensor_id):
    if request.user.is_authenticated:
        try:
            sensor = Sensor.objects.filter(owner=request.user).get(id=sensor_id)
        except Sensor.DoesNotExist:
            return Response({"error": "Sensor Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)
        items = DataPoint.objects.filter(sensor=sensor)
        serializer = DataPointSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def add_data(request):
    if request.user.is_authenticated:
        try:
            Sensor.objects.filter(owner=request.user).get(id=request.data["sensor"])
        except Sensor.DoesNotExist:
            return Response({"error": "Sensor Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DataPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=status.HTTP_200_OK)
        # return Response("Invalid Data", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)