from django.db import models

class MenuItem(models.Model):
    # the specified restaurant would be the foreign key to connect menu items with the restaurants
    menu_item_name = models.CharField(max_length=200)
    menu_item_description = models.CharField(max_length=200)
    menu_item_price = models.IntegerField(default=0)

    def __str__(self):
        return self.menu_item_name
class Restaurant(model.Model):
    #the restaurant's name and login info
    restaurant_name = models.CharField(max_length=200)
    restaurant_username = models.CharField(max_length=30)
    restaurant_password = models.CharField(max_length=50, min_length=8)

# Create your models here.
