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
        
        # url = reverse('website:register')
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, 200)
#        login = self.client.login(username='username', password = 'password')

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
        # self.client.login(username='username', password = 'password')
      #  path = reverse('register:login')
    #    response = HttpRedirectReponse()
        # request.user = Restaurant.objects.create()
        # response.POST['restaurant_name'] = 'restaurant'
        # response.POST['restaurant_username'] = 'username'
        # # response.POST['restaurant_password'] = 'password'   
        # response = self.client.post('accounts/register/',
        #      #data={'restaurantname':'restaurant', 'username':'username', 'password': 'password'})  
        # print('buttface')
        # print(response)
        # self.assertRedirects(response, 'accounts/login/')
  # client = Client()
   #   response = self.client.post('accounts/register/')
  #  self.assertEqual(response.get('accounts/register'), 'accounts/login')


class AddMenuItemTest(TestCase):


    def test_add_menu_item(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        restaurant_id = str(database.id)

        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': restaurant_id}), 
            {
            'menuitemname':'test1', 
            'menuitemdescription':'testing 1', 
            'menuitemprice': 1,
            }, follow = True)
        print('HELLO there')
        # print(MenuItem.objects.get(menu_item_name = 'test1'))
        print(response)
        self.assertEqual(MenuItem.objects.count(), 1)

        # redirect_url = "/website/edit_menu/" + str(restaurant_id)
        # self.assertRedirects(response, redirect_url)
