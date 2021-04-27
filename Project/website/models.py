from django.db import models

class MenuItem(models.Model):
    # the specified restaurant would be the foreign key to connect menu items with the restaurants
    menu_item_name = models.CharField(max_length=200)
    menu_item_description = models.CharField(max_length=200)
    menu_item_price = models.IntegerField(default=0)

    def __str__(self):
        return self.menu_item_name

# Create your models here.
