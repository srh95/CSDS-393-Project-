from django.db import models

class MenuItem(model.Model):
    menu_item_name = models.CharField(max_length=200)
    menu_item_description = models.CharField(max_length=200)
    menu_item_price = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text

# Create your models here.
