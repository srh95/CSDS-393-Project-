from django.test import TestCase, Client
from django.urls import reverse, path


from website.forms import (
    RegisterForm,
    LoginForm,
    SearchForm
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
    # simulate a user entering in a valid form and being redirected to login successfully
    def test_restaurant_created(self):
        response = self.client.post(reverse('website:register'), 
            {
            'restaurantname':'restaurant', 
            'username':'username', 
            'password1': 'password',
            'password2': 'password'
            }, follow = True)
        # print('right here buttface')
        # print(response)
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

        # print('HELLO there')
        # # print(MenuItem.objects.get(menu_item_name = 'test1'))
        # print(response)

        redirect_url = "/website/restaurant/" + str(restaurant_id) + "/"

        self.assertRedirects(response, redirect_url)

class SearchbarTest(TestCase):
    def test_no_restaurants_exist(self):
        # simulate a user searching for a restaurant called 'restaurant'
        # no results found so restaurant homepage html is returned
        response = self.client.post(reverse('website:search'),
            {
            'restaurantsearch':'restaurant2', 
            }, follow = True)
        self.assertTemplateUsed(response, 'website/searchbar.html')
        
    def test_no_restaurants_from_search(self):
        # simulate a user searching for a restaurant called 'restaurant'
        # no results found so restaurant homepage html is returned
        database = Restaurant.objects.create(
            restaurant_name = 'restaurant',
            restaurant_username = 'username',
            restaurant_password = 'password',
        )    
        response = self.client.post(reverse('website:search'),
            {
            'restaurantsearch':'restaurant2', 
            }, follow = True)
        self.assertTemplateUsed(response, 'website/searchbar.html')
        # self.assertInHTML('/website/templates/website/restaurants.html', response.content.decode())


    def test_one_restaurant_found(self):
        # simulate a user searching for a restaurant called 'restaurant'
        # one result found so searchbar html is returned
        database = Restaurant.objects.create(
            restaurant_name = 'restaurant',
            restaurant_username = 'username',
            restaurant_password = 'password',
        )        
        response = self.client.post(reverse('website:search'),
            {
            'restaurantsearch':'restaurant', 
            }, follow = True)
        self.assertTemplateUsed(response, 'website/searchbar.html')


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
        # print('HELLO there')
        # # print(MenuItem.objects.get(menu_item_name = 'test1'))
        # print(response)
        self.assertEqual(MenuItem.objects.count(), 1)

        redirect_url = "/website/restaurant/" + str(restaurant_id) + "/"
        self.assertRedirects(response, redirect_url)

    
