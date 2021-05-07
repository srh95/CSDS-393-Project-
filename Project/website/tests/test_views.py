from django.test import TestCase, Client
from django.urls import reverse, path


from website.forms import (
    RegisterForm,
    LoginForm,
    SearchForm,
    AddToCartForm,
    RemoveFromCartForm,
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

    def test_update_menu_item_name(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA2',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        og_menu_item = MenuItem.objects.create(
            restaurant_id = database.id,
            menu_item_name = "original",
            menu_item_description = "original description",
            menu_item_price = 1
        )

        menu_id = og_menu_item.id

        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': og_menu_item.id}), 
            {
            'menuitemname':'updated', 
            }, follow = True)


        print(response)

        updated_name = MenuItem.objects.get(id = menu_id)

        self.assertEqual(updated_name.menu_item_name, 'updated')

class ReservationTest(TestCase):

    def test_create_reservation(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        restaurant_id = str(database.id)

        response = self.client.post(reverse('website:create_reservation', kwargs={'restaurant_id': restaurant_id}),
            {
            'table_id':'60',
            'num_people':'4',
            'date': '2021-04-19',
            'time' : '6:00'
            }, follow = True)

        self.assertEqual(ReservationSlot.objects.count(), 1)


    def test_reserve_table(self):
        restaurant = Restaurant.objects.create(
            restaurant_name='SARA',
            restaurant_username='username',
            restaurant_password='password',
        )

        reservation = ReservationSlot.objects.create(
            table_id = '06',
            num_people = 7,
            date = '2022-04-19',
            time = '7:00',
        )

        restaurant_id = str(restaurant.id)
        reservation_id = str(reservation.id)
        response = self.client.post(reverse('website:confirm_reservation', kwargs={'reservation_id': reservation_id}),
                                    {
                                         'name': 'sophia',
                                         'email': 'soph@gmail.com',
                                         'phone': 2484259066,
                                    }, follow=True)
        # print('sophia')
        object = ReservationSlot.objects.get(name='sophia')
        print('made this reservation')
        print(object.name)
        self.assertEqual(object.name, 'sophia')

    def test_search_reservation(self):
        restaurant = Restaurant.objects.create(
            restaurant_name='SARA',
            restaurant_username='username',
            restaurant_password='password',
        )

        reservation = ReservationSlot.objects.create(
            table_id='06',
            num_people=7,
            date='2022-04-19',
            time='7:00',
        )
        restaurant_id = str(restaurant.id)
        reservation_id = str(reservation.id)
        response = self.client.post(reverse('website:reserve_table', kwargs={'restaurant_id': restaurant_id}),
                                    {
                                        'date': '2022-04-19',
                                    },follow=True)

        object = ReservationSlot.objects.get(date='2022-04-19')
        print('this is the date')
        print(str(object.date))

        # for reservation in response :
        #
        self.assertEqual(str(object.date),'2022-04-19')

