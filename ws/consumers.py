import json
import math
from pprint import pprint

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token

from api.serializers import DataPointSerializer
from main.models import Sensor, DataPoint


class SensorConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.sensor_id = None

    def connect(self):
        for header in self.scope["headers"]:
            if header[0] == b'authorization':
                print("Authorization header found")
                t = header[1].split(b' ')[1].decode()
                try:
                    token = Token.objects.get(key=t)
                    self.scope['user'] = token.user
                    print("Valid Token")
                except Token.DoesNotExist:
                    print("Invalid token")
            if header[0] == b'sensor':
                print("Sensor header found")
                self.sensor_id = int(header[1].decode())

        if self.scope["user"].is_authenticated and self.sensor_id is not None:
            try:
                Sensor.objects.filter(owner=self.scope['user']).get(id=self.sensor_id)
                self.accept()
            except Sensor.DoesNotExist:
                print(f"Sensor {self.sensor_id} Does Not Exists")
                self.close()
        else:
            self.close()

    def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        dataset = json.loads(text_data)
        invalid = False
        new_dataset = []
        for datapoint in dataset:
            try:
                new_dataset.append({
                    'date': datapoint["dt"],
                    'temperature': datapoint["tm"],
                    'humidity': datapoint["hm"],
                    'pressure': datapoint["pr"],
                    'air_speed': datapoint["as"],
                    'air_direction': datapoint["ad"],
                    'sensor': self.sensor_id,
                })
            except KeyError:
                invalid = True
                break
        if not invalid:
            serializer = DataPointSerializer(data=new_dataset, many=True)
            if serializer.is_valid():
                serializer.save()
                self.send(text_data="ok")
                print("received data")
            else:
                self.send(text_data="err")
                print("received data not valid")
        else:
            self.send(text_data=json.dumps("err"))
            print("Invalid Data")
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            f"Plotter-{self.sensor_id}", {'type': 'send_data'}
        )


class PlotterConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.sensor_id = None
        self.limit = 500
        self.offset = 0

    def connect(self):
        self.sensor_id = self.scope['url_route']['kwargs']['sensor_num']
        self.room_group_name = f"Plotter-{self.sensor_id}"
        if self.scope['user'].is_authenticated:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        self.sensor_id = text_data_json["sensor_id"]
        self.limit = text_data_json["limit"]
        self.offset = text_data_json["offset"]

        self.send_data()

    def send_data(self, event=None):
        try:
            sensor = Sensor.objects.filter(owner=self.scope['user']).get(id=self.sensor_id)
        except Sensor.DoesNotExist:
            self.send(text_data=json.dumps({
                "code": 404,
                "error": "Sensor Does Not Exists"
            }))
            return
        items = DataPoint.objects.filter(sensor=sensor).order_by('-date')
        skip_every = math.ceil(self.limit / 500)
        xx = list(items[self.offset:self.offset + self.limit:skip_every])
        serializer = DataPointSerializer(xx, many=True)
        self.send(text_data=json.dumps({
            'code': 200,
            'data': serializer.data
        }))
