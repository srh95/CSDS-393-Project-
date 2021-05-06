from django.test import TestCase
from website.forms import RegisterForm
from website.models import (
    Order,
    OrderItem,
    MenuItem,
    Restaurant,
    ReservationSlot,
    Table
)
from django.contrib import messages

# Create your tests here.


class RegisterFormTest(TestCase):
    def test_restaurant_exists(self):
        database = Restaurant.objects.create(
        restaurant_name = 'test'
        )
        form = RegisterForm()
        form.fields['restaurantname'] = 'test'
        self.assertEqual(getattr(database, 'restaurant_name'), form.fields['restaurantname'])

    def test_passwords_dont_match(self):
        form = RegisterForm()
        form.fields['password1'] = 'password'
        form.fields['password2'] = 'password'
        self.assertTrue(form.fields['password1'] == form.fields['password2'])
        

