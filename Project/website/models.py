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

    def __str__(self):
        return self.menu_item_name


# putting items in an order
class OrderItem(models.Model):
    #default_restaurant_id = 0
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True,blank=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True,blank=True)
    #table = models.OneToOneField(Table, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length = 200, default='00000')
    item_price = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    item_removed = models.BooleanField(default=False)
    item_number = models.IntegerField(default=1)

    def __repr__(self):
        return self.item_price

    def __str__(self):
        return self.item_name
  #  start_date = models.DateTimeField(auto_now_add = True)
   # ordered_date = models.DateTimeField()
 #   ordered = models.BooleanField(default = False)

    # def __str__(self):
    #     return self.user.username

# Reservation
class ReservationSlot(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    table_id = models.CharField(max_length=2)
    num_people = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    booked = models.BooleanField(default=False)
    name = models.CharField(max_length=50, default="N/A")
    email = models.EmailField(default="")
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.table_id
    
class Table(models.Model):
    #default_restaurant_id = 0
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    #order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    table_number = models.IntegerField(default=0)
    #order_list = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.table_number
