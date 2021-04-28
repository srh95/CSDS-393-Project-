from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import MenuItem
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import Restaurant
from .forms import RegisterForm
from django.core.exceptions import ValidationError

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
    context = {'restaurant' : restaurant}
    return render(request, 'website/restaurant.html', context)

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
            return HttpResponseRedirect('/website/accounts/login/')
    else:
        form = RegisterForm()
        context = {'form' : form}
    return render(request, 'website/register.html', context)
