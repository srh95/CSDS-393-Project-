from django.db import models
from django.conf import settings
from django.utils import timezone

class Restaurant(models.Model):
    #the restaurant's name and login info
    restaurant_name = models.CharField(max_length=200)
    restaurant_username = models.CharField(max_length=30)
    restaurant_password = models.CharField(max_length=50)


class MenuItem(models.Model):
    # the specified restaurant would be the foreign key to connect menu items with the restaurants
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_item_name = models.CharField(max_length=200)
    menu_item_description = models.CharField(max_length=200)
    menu_item_price = models.FloatField(default=0)
 #   inOrder = models.BooleanField(default=false)

    def __str__(self):
        return self.menu_item_name


# putting items in an order
class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
  #  start_date = models.DateTimeField(auto_now_add = True)
   # ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

# Reservation
class ReservationSlot(models.Model):
    table_id = models.CharField(max_length=2)
    num_people = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    booked = models.BooleanField(default=False)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField(default="")
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.table_id
    

