from django.contrib import admin
from .models import MenuItem
from .models import Restaurant
from .models import Order

admin.site.register(MenuItem)
admin.site.register(Restaurant)
admin.site.register(Order)
