import csv

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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
        return render(request, 'main/login.html', )


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
    # datapoint = DataPoint.objects.filter(sensor=sensors).order_by('-date')[:100]
    context = {
        'sensors': sensors,
        # 'datapoint': datapoint
    }
    return render(request, 'main/sensor.html', context)


def get_sensor_data(request, sensor_num):
    if not request.user.is_authenticated:
        return render(request, 'main/login.html')
    if request.method != "POST":
        raise Http404("GET request is not supported")
    try:
        sensors = Sensor.objects.filter(owner=request.user).get(id=sensor_num)
    except Sensor.DoesNotExist:
        raise Http404("Sensor does not exists")
    ranges = {
        '1': 100,
        '2': 500,
        '3': 1000,
        '4': 10000,
        '5': 999999,
    }
    data_range = ranges.get(request.POST.get('range', '1'), 10)
    datapoint = DataPoint.objects.filter(sensor=sensors).order_by('-date')[:data_range]
    field_names = [field.name for field in datapoint.model._meta.fields]
    keep = ['date'] + [name for name in field_names if name in request.POST]
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="Sensor_{sensor_num}.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(keep)
    for obj in datapoint:
        writer.writerow([getattr(obj, field) for field in keep])

    return response


def delete_sensor_data(request, sensor_num):
    t = DataPoint.objects.filter(sensor_id=sensor_num).delete()
    try:
        r = f"Sensor {sensor_num} datapoints deleted {t}"
    except:
        r = "Error"
    return HttpResponse(r)

