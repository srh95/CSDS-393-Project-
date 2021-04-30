from django.db import models
from django.conf import settings
from django.utils import timezone
# from website.models import Restaurant

class Table(models.Model):
    # restaurant is foreign key to connect
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table_number = models.IntegerField(default=0)
