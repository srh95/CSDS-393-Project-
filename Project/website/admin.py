from django.contrib import admin
from .models import (
    MenuItem,
    Restaurant,
    Order,
    OrderItem,
    ReservationSlot,
    Table
)

admin.site.register(MenuItem)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ReservationSlot)
admin.site.register(Table)
