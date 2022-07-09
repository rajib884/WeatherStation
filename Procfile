web: daphne WeatherStation.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=WeatherStation.settings -v2
release: python manage.py migrate