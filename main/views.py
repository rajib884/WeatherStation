from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import DataPoint


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'main/login.html')
    datapoint = DataPoint.objects.order_by('-date')[0]
    context = {
        'datapoint': datapoint
    }
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
    pprint(request.GET)
    if sensor_num > 2:
        raise Http404("Sensor does not exists")
    return HttpResponse(f"Sensor {sensor_num}")
