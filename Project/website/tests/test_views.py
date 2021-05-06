from django.test import TestCase, Client
from django.urls import reverse, path


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

class RegisterTest(TestCase):

    def test_restaurant_created(self):
        # simulate a user entering in a valid form and being redirected to login successfully
        response = self.client.post(reverse('website:register'), 
            {
            'restaurantname':'restaurant', 
            'username':'username', 
            'password1': 'password',
            'password2': 'password'
            }, follow = True)
        print('right here buttface')
        print(response)
        self.assertRedirects(response, '/website/accounts/login/')

class LoginTest(TestCase):
    # simulate a user entering in an existing restaurant's account information
    # successfully redirect to that restaurant's homepage
    def test_login_worked(self):
        database = Restaurant.objects.create(
            restaurant_name = 'restaurant',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )
        restaurant_id = str(database.id)

        response = self.client.post(reverse('website:login'),
            {
            'restaurantname':'restaurant', 
            'username':'username', 
            'password': 'password',
            }, follow = True)

        print('HELLO there')
        # print(MenuItem.objects.get(menu_item_name = 'test1'))
        print(response)

        redirect_url = "/website/restaurant/" + str(restaurant_id) + "/"

        self.assertRedirects(response, redirect_url)

class MenuItemTest(TestCase):


    def test_add_menu_item(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        restaurant_id = str(database.id)

        response = self.client.post(reverse('website:addmenuitem', kwargs={'restaurant_id': restaurant_id}), 
            {
            'menuitemname':'test1', 
            'menuitemdescription':'testing 1', 
            'menuitemprice': 1,
            }, follow = True)
        print('HELLO there')
        # print(MenuItem.objects.get(menu_item_name = 'test1'))
        print(response)
        self.assertEqual(MenuItem.objects.count(), 1)

        redirect_url = "/website/restaurant/" + str(restaurant_id) + "/"
        self.assertRedirects(response, redirect_url)

    
