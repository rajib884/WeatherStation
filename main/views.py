from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import DataPoint, Sensor


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'main/login.html')
    sensors = Sensor.objects.filter(owner=request.user)
    context = {'sensors': sensors}
    return render(request, 'main/index.html', context)


def user_login(request):
    logout(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main:index', args=None))
            # return render(request, 'main/login.html',)
        else:
            return render(request, 'main/login.html', {'failed_login': True})
    else:
        return render(request, 'main/login.html',)


def user_logout(request):
    logout(request)
    return render(request, 'main/login.html')


def sensor(request, sensor_num):
    if not request.user.is_authenticated:
        return render(request, 'main/login.html')
    try:
        sensors = Sensor.objects.filter(owner=request.user).get(id=sensor_num)
    except Sensor.DoesNotExist:
        raise Http404("Sensor does not exists")
    datapoint = DataPoint.objects.filter(sensor=sensors).order_by('-date')[:100]
    context = {
        'sensors': sensors,
        'datapoint': datapoint
    }
    return render(request, 'main/sensor.html', context)
