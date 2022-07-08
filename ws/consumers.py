import json
import math

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token

from api.serializers import DataPointSerializer
from main.models import Sensor, DataPoint


class SensorConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        dataset = json.loads(text_data)
        response = {
            "code": 200,
            "msg": "ok"
        }

        if 'type' in dataset:
            if dataset['type'] == 'data':
                if self.scope['user'].is_authenticated:
                    data = json.loads(dataset['data'])
                    for datapoint in data:
                        try:
                            Sensor.objects.filter(owner=self.scope['user']).get(id=datapoint["sensor"])
                        except Sensor.DoesNotExist:
                            print({"error": f"Sensor {datapoint['sensor']} Does Not Exists"})
                            response = {
                                "code": 404,
                                "msg": f"Sensor {datapoint['sensor']} Does Not Exists"
                            }
                            break
                    if response['code'] == 200:
                        serializer = DataPointSerializer(data=data, many=True)
                        if serializer.is_valid():
                            serializer.save()
                else:
                    response = {
                        "code": 404,
                        "msg": f"User unauthenticated"
                    }
            elif dataset['type'] == 'token':
                try:
                    token = Token.objects.get(key=dataset["token"])
                    self.scope['user'] = token.user
                    response = {
                        "code": 200,
                        "msg": "Valid Token"
                    }
                except Token.DoesNotExist:
                    response = {
                        "code": 404,
                        "msg": "Invalid Token"
                    }
            else:
                response = {
                    "code": 404,
                    "msg": f"Invalid type"
                }
        else:
            response = {
                "code": 404,
                "msg": "Send 'type'"
            }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            "Plotter", {'type': 'send_data'}
        )
        self.send(text_data=json.dumps(response))
        print(response)


class PlotterConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = "Plotter"
        self.sensor_id = None
        self.limit = 500
        self.offset = 0

    def connect(self):
        # pprint(self.scope['user'])
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
