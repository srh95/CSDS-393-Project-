from django.test import TestCase
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

# Create your tests here.


class RegisterFormTest(TestCase):
    def test_restaurant_already_exists(self):
        database = Restaurant.objects.create(
        restaurant_name = 'test'
        )
        form = RegisterForm()
        form.fields['restaurantname'] = 'test'
        #getting database's restaurant name and comparing it with the form restaurant name
        self.assertEqual(getattr(database, 'restaurant_name'), form.fields['restaurantname'])

    def test_passwords_dont_match(self):
        form = RegisterForm()
        form.fields['password1'] = 'password'
        form.fields['password2'] = 'password_wrong'
        # comparing the form's first password entry with its second password entry
        self.assertNotEqual(form.fields['password1'], form.fields['password2'])

        

class LoginFormTest(TestCase):

    def test_restaurant_name_not_found(self):
        database = Restaurant.objects.create(
        restaurant_name = 'restaurant',
        restaurant_username = 'username',
        restaurant_password = 'password'
        )
        form = LoginForm()
        form.fields['restaurantname'] = 'restaurant_wrong'
        form.fields['username'] = 'username'
        form.fields['password'] = 'password'      
        # comparing the database's restaurant name with the inputted restaurant name
        self.assertNotEqual(getattr(database, 'restaurant_name'), form.fields['restaurantname'])
    
    def test_username_doesnt_match(self):
        database = Restaurant.objects.create(
        restaurant_name = 'restaurant',
        restaurant_username = 'username',
        restaurant_password = 'password'
        )
        form = LoginForm()
        form.fields['restaurantname'] = 'restaurant'
        form.fields['username'] = 'username_wrong'
        form.fields['password'] = 'password'
        # comparing the database's username with the inputted username
        self.assertNotEqual(getattr(database, 'restaurant_username'), form.fields['username'])

    def test_password_doesnt_match(self):
        database = Restaurant.objects.create(
        restaurant_name = 'restaurant',
        restaurant_username = 'username',
        restaurant_password = 'password'
        )
        form = LoginForm()
        form.fields['restaurantname'] = 'restaurant'
        form.fields['username'] = 'username'
        form.fields['password'] = 'password_wrong'
        # comparing the database's username with the inputted username
        self.assertNotEqual(getattr(database, 'restaurant_password'), form.fields['password'])
        

class ReservationTest(TestCase) :
    def test_valid_reservationform(self):
        rs = ReservationSlot.objects.create(table_id = '89',num_people = '1',date = '2022-04-19',time = '3:00')
        data = {'table_id': rs.table_id, 'num_people' : rs.num_people, 'date' : rs.date, 'time' : rs.time}
        form = CreateReservationForm()
        self.assertTrue(form.isvalid())

    def test_invalid_reservationform(self):
        rs = ReservationSlot.objects.create(table_id='89', num_people='1', date='04/19/2022', time='3:00')
        data = {'table_id': rs.table_id, 'num_people' : rs.num_people, 'date' : rs.date, 'time' : rs.time}
        form = CreateReservationForm()
        self.assertFalse(form.isvalid())



