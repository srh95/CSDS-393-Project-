from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import Restaurant

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
    context = {'restaurant' : restaurant, 'menu_list' : menu_list}
    return render(request, 'website/restaurant.html', context)