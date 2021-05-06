from django.test import TestCase, Client
from website.forms import (
    RegisterForm,
    LoginForm
)
from website.models import (
    Order,
    OrderItem,
    MenuItem,
    Restaurant,
    ReservationSlot,
    Table
)
from django.contrib import messages
from django.urls import reverse
from budget.models importt Project, Category, Expense
import json

