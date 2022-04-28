from django.db import models
import pytz


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)


class DataPoint(models.Model):
    date = models.DateTimeField("Date Collected", auto_created=True, primary_key=True)
    temperature = models.FloatField("Temperature")
    humidity = models.IntegerField("Humidity")
    pressure = models.IntegerField("Pressure")

    def __str__(self):
        return self.date.astimezone(pytz.timezone("Asia/Dhaka")).strftime("%Y-%m-%d %H:%M:%S GMT%Z")
