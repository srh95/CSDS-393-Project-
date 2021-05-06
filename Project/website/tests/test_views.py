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
