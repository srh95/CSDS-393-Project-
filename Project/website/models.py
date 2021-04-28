from django.db import models

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
    menu_item_price = models.IntegerField(default=0)

    def __str__(self):
        return self.menu_item_name

# Create your models here.
