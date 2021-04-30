from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm
from .forms import AddMenuItemForm
from .forms import LoginForm
from .forms import UpdateMenuItemNameForm
from .forms import UpdateMenuItemDescriptionForm
from .forms import UpdateMenuItemPriceForm
from django.core.exceptions import ValidationError
from .models import (
    Order,
    OrderItem,
    MenuItem,
    Restaurant
)
from django.views.generic import ListView, DetailView, View
from django.utils import timezone


def index(request):
    return HttpResponse("Hello, world. You're at the website index.")

def menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    return render(request, 'website/menu_item.html', {'menu_item': menu_item})

def menu_list(request):
    menu_list = MenuItem.objects.all()
    context = {'menu_list': menu_list,}
    return render(request, 'website/menu_list.html', context)

def restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_list = MenuItem.objects.filter(restaurant__pk = restaurant_id)
    context = {'restaurant' : restaurant, 'menu_list' : menu_list, 'restaurant_id' : restaurant_id}
    return render(request, 'website/restaurant.html', context)

def restaurant_list(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurant_list': restaurant_list,}
    return render(request, 'website/restaurants.html', context)

def add_menu_item(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_list = MenuItem.objects.filter(restaurant__pk = restaurant_id)
    if request.method == 'POST':
        form = AddMenuItemForm(request.POST)
        if form.is_valid():
            database = MenuItem.objects.create(
            restaurant = restaurant,
            menu_item_name = form.cleaned_data['menuitemname'],
            menu_item_description = form.cleaned_data['menuitemdescription'],
            menu_item_price = form.cleaned_data['menuitemprice']
            )
            database.save()
            url = '/website/restaurant/' + str(restaurant_id)
            return HttpResponseRedirect(url)
    else:
        form = AddMenuItemForm()
        context = {'form' : form, 'menu_list' : menu_list, 'restaurant_id' : restaurant_id}
    return render(request, 'website/edit_menu.html', context)

def edit_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    if request.method=='POST' and 'btnform1' in request.POST:
        form = UpdateMenuItemNameForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['menuitemname'])
            menu_item.menu_item_name = form.cleaned_data['menuitemname']
            menu_item.save(update_fields=['menu_item_name'])
            url = '/website/restaurant/menu_list/' + str(menu_item.id)
            return HttpResponseRedirect(url)
    
    if request.method=='POST' and 'btnform2' in request.POST:
        form = UpdateMenuItemDescriptionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['menuitemdescription'])
            menu_item.menu_item_description = form.cleaned_data['menuitemdescription']
            menu_item.save(update_fields=['menu_item_description'])
            url = '/website/restaurant/menu_list/' + str(menu_item.id)
            return HttpResponseRedirect(url)

    if request.method=='POST' and 'btnform3' in request.POST:
        form = UpdateMenuItemPriceForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['menuitemprice'])
            menu_item.menu_item_price = form.cleaned_data['menuitemprice']
            menu_item.save(update_fields=['menu_item_price'])
            url = '/website/restaurant/menu_list/' + str(menu_item.id)
            return HttpResponseRedirect(url)

    else:
        form = UpdateMenuItemDescriptionForm()
    return render(request, 'website/edit_menu_item.html', {'form': form, 'menu_item' : menu_item,})

    # if request.method=='POST' and 'btnform2' in request.POST:
    

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if(form.cleaned_data['password1'] != form.cleaned_data['password2']):
                raise ValidationError('Passwords do not match')
            database = Restaurant.objects.create(
            restaurant_name = form.cleaned_data['restaurantname'],
            restaurant_username = form.cleaned_data['username'],
            restaurant_password = form.cleaned_data['password1']
            )
            database.save()
            return HttpResponseRedirect('/website/restaurant/')
    else:
        form = RegisterForm()
        context = {'form' : form}
    return render(request, 'website/register.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                if(Restaurant.objects.get(restaurant_username=username)):
                    restaurant = Restaurant.objects.get(restaurant_username=username)
                    if(restaurant.restaurant_password != password):
                        raise ValidationError('Incorrect username or password')
                    url = '/website/restaurant/' + str(restaurant.id)
                    return HttpResponseRedirect(url)
            except ObjectDoesNotExist:
                raise ValidationError('Incorrect username or password')
            # if(username != Restaurant.objects.all().filter(restaurant_username=username)
            #     or password != Restaurant.objects.all().filter(restaurant_password=password)):
            #     raise ValidationError('Account not found')
            # return HttpResponseRedirect('/website/restaurant/<int:restaurant_id>/')
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form': form})


def add(request, id):
        item = get_object_or_404(MenuItem)
        order_item = MenuItem.objects.create(item=item)
    #    order_qs = Order.objects.filter(user=request.user, ordered=False)
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)  

def remove(request):
        item = get_object_or_404(MenuItem)
        order_item = MenuItem.objects.filter(item=item, user=request.user)
        order.items.remove(order_item)
        
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'order_summary.html')
    model = Order
    template_name = 'order_summary.html'

def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        restaurant = Restaurant.objects.all().filter(restaurant_name=search)
        return render(request, 'website/searchbar.html', {'restaurant': restaurant})

