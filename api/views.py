import math
import time

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import SensorSerializer, DataPointSerializer, UserSerializer
from main.models import Sensor, DataPoint


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_sensor(request):
    if request.user.is_authenticated:
        items = Sensor.objects.filter(owner=request.user)
        serializer = SensorSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request, sensor_id):
    paginator = LimitOffsetPagination()
    paginator.offset_query_param = "offset"
    paginator.default_limit = 500
    paginator.limit_query_param = "limit"

    if request.user.is_authenticated:
        try:
            sensor = Sensor.objects.filter(owner=request.user).get(id=sensor_id)
        except Sensor.DoesNotExist:
            return Response({"error": "Sensor Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)
        items = DataPoint.objects.filter(sensor=sensor).order_by('-date')
        res_pg = paginator.paginate_queryset(items, request)
        xx = []
        div = math.ceil(len(res_pg) / 500)
        for i, item in enumerate(res_pg):
            if i % div == 0:
                xx.append(item)
        serializer = DataPointSerializer(xx, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
        return Response("Invalid Data", status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_time(requests):
    return Response(int(time.time()) - 946684800 + 6*3600)


@api_view(['POST'])
def check_token(request):
    if 'token' in request.data:
        try:
            Token.objects.get(key=request.data['token'])
            return Response(True, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(False, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_sensor_id(request):
    if request.user.is_authenticated:
        try:
            Sensor.objects.filter(owner=request.user).get(id=request.data["sensor"])
        except Sensor.DoesNotExist:
            return Response(False, status=status.HTTP_404_NOT_FOUND)
        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
