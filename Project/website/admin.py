from django.contrib import admin
from .models import MenuItem
from .models import Restaurant
from .models import Order
from .models import OrderItem


admin.site.register(MenuItem)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(OrderItem)


