from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, View
import datetime
from django.utils import timezone
from .forms import (
    RegisterForm,
    AddMenuItemForm,
    LoginForm,
    UpdateMenuItemNameForm,
    UpdateMenuItemDescriptionForm,
    UpdateMenuItemPriceForm,
    AddToCartForm,
    SearchForm,
    RemoveFromCartForm,
    ReserveTableForm,
    CreateReservationForm,
    PaymentSuccess,
    CreateTableForm,
    CloseTableForm
)
from .models import (
    Order,
    OrderItem,
    MenuItem,
    Restaurant,
    ReservationSlot,
    Table
)


def index(request):
    return HttpResponse("Hello, world. You're at the website index.")

def menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['num_items'])
            print(menu_item.menu_item_name)
            print(menu_item.menu_item_price)
            tmpNum = 0
            for x in range(form.cleaned_data['num_items']):
                print('create thingy here')
                database = Order.objects.create(
                    item_name = menu_item.menu_item_name,
                    item_price = menu_item.menu_item_price,
                    item_number = tmpNum
                )
                database.save()
                tmpNum = tmpNum+1
            url = '/website/restaurant/' + str(menu_item.restaurant_id)
            return HttpResponseRedirect(url)

    else:
        form = AddToCartForm()
    return render(request, 'website/menu_item.html', {'menu_item': menu_item})

def menu_list(request):
    menu_list = MenuItem.objects.all()
    context = {'menu_list': menu_list,}
    return render(request, 'website/menu_list.html', context)

def order_summary(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    context = {'restaurant': restaurant_list}
    return render(request, 'website/order_summary.html')

def order_list(request):
    order_list = Order.objects.all()
    order_list_price = 0
    if request.POST:
        items_removed = request.POST.getlist('items_removed')
        form = RemoveFromCartForm(request.POST)
        if form.is_valid():
            for x in items_removed:
                print(x)
                instance = Order.objects.filter(item_name=x)
                instance[0].delete()
    for x in order_list:
        price = x.__repr__()
        price = float(price)
        order_list_price = order_list_price + price
    print(order_list_price)
    order_list_price = str(order_list_price)
    context = {'order_list': order_list, 'order_list_price': order_list_price}
    return render(request, 'website/order_summary.html', context)

def paymentSuccess(request):
    #if request.POST:
    Order.objects.all().delete()
    return render(request, 'website/successPage.html')

def remove_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    order_list = Order.objects.all()
    if request.method == 'POST':
        form = RemoveFromCartForm(request.POST)
        if form.is_valid:
            for x in order_list:
                if x == menu_item:
                    x.delete()
                    break

def restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_list = MenuItem.objects.filter(restaurant__pk = restaurant_id)
    context = {'restaurant' : restaurant, 'menu_list' : menu_list, 'restaurant_id' : restaurant_id}
    return render(request, 'website/restaurant-business-side.html', context)

def restaurant_user_side(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_list = MenuItem.objects.filter(restaurant__pk = restaurant_id)
    context = {'restaurant' : restaurant, 'menu_list' : menu_list, 'restaurant_id' : restaurant_id}
    return render(request, 'website/restaurant-user-side.html', context)

def restaurant_list(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurant_list': restaurant_list}
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
            url = '/website/restaurant/edit_menu/' + str(menu_item.restaurant_id)
            return HttpResponseRedirect(url)
    
    if request.method=='POST' and 'btnform2' in request.POST:
        form = UpdateMenuItemDescriptionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['menuitemdescription'])
            menu_item.menu_item_description = form.cleaned_data['menuitemdescription']
            menu_item.save(update_fields=['menu_item_description'])
            url = '/website/restaurant/edit_menu/' + str(menu_item.restaurant_id)
            return HttpResponseRedirect(url)

    if request.method=='POST' and 'btnform3' in request.POST:
        form = UpdateMenuItemPriceForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['menuitemprice'])
            menu_item.menu_item_price = form.cleaned_data['menuitemprice']
            menu_item.save(update_fields=['menu_item_price'])
            url = '/website/restaurant/edit_menu/' + str(menu_item.restaurant_id)
            return HttpResponseRedirect(url)

    else:
        form = UpdateMenuItemDescriptionForm()
    return render(request, 'website/edit_menu_item.html', {'form': form, 'menu_item' : menu_item, 'restaurant_id' : menu_item.restaurant_id})

def delete_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    if request.method == "POST":
        menu_item.delete()
        url = '/website/restaurant/' + str(menu_item.restaurant_id)
        return redirect(url)

    context={'menu_item' : menu_item}
    return render(request, 'website/delete_menu_item.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if(form.cleaned_data['password1'] != form.cleaned_data['password2']):
                messages.error(request, 'Passwords do not match')
                return HttpResponseRedirect('/website/accounts/register/')
                #raise ValidationError('Passwords do not match')
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

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            restaurant = form.cleaned_data['restaurantname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                if(Restaurant.objects.get(restaurant_name=restaurant) is None):
                    messages.error(request, 'Incorrect username or password, or this restaurant does not exist')
                    return HttpResponseRedirect('/accounts/login/')
                if(Restaurant.objects.get(restaurant_username=username)):
                    restaurant = Restaurant.objects.get(restaurant_username=username)
                    if(restaurant.restaurant_password != password):
                        messages.error(request, 'Incorrect username or password, or this restaurant does not exist')
                        return HttpResponseRedirect('/accounts/login/')
                       # raise ValidationError('Incorrect username or password')
                    url = '/website/restaurant/' + str(restaurant.id)
                    return HttpResponseRedirect(url)
            except ObjectDoesNotExist:
                    messages.error(request, 'Incorrect username or password, or this restaurant does not exist')
                    return HttpResponseRedirect('/accounts/login/')
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form': form})


def add_to_cart(request, id):
 #       form = AddToCartForm(request.POST)
  #      if form.is_valid()

        item = get_object_or_404(MenuItem)
        order_item = OrderItem.objects.create(item=item)

    #    order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user)
        if(order_qs.exists()):
            order = order_qs[0]
        else:
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)
        url = '/website/restaurant/menu_list/' + str(item.id)
        return HttpResponseRedirect(url)

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
    restaurant_list = Restaurant.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['restaurantsearch'])
            user_search = form.cleaned_data['restaurantsearch']
            matching_restaurants = Restaurant.objects.filter(restaurant_name__icontains=user_search)
            print(matching_restaurants)
            return render(request, 'website/searchbar.html', {'form' : form, 'matching_restaurants': matching_restaurants})
    else:
        form = SearchForm()
        return render(request, 'website/restaurants.html', {'form' : form, 'restaurant_list': restaurant_list}) 

# Searches for reservations by date
def reserve_table(request,restaurant_id):
    # reservation_slots = ReservationSlot.objects.filter(restaurant__pk=restaurant_id)
    if request.method == 'GET':
            date = request.GET.get('date')
            reservation_slots = ReservationSlot.objects.filter(date=date, restaurant__pk=restaurant_id)

    return render(request, 'website/reservation.html', {'reservation_slots': reservation_slots,'mydate' : date})

# for creating a reservation slot
def create_reservation(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    reservation_slots = ReservationSlot.objects.filter(restaurant__pk=restaurant_id)
    create_form = CreateReservationForm()
    if request.method == 'POST':
        create_form = CreateReservationForm(request.POST)
        if create_form.is_valid():
            database = ReservationSlot.objects.create(
            restaurant = restaurant,
            table_id = create_form.cleaned_data['table_id'],
            num_people = create_form.cleaned_data['num_people'],
            time = create_form.cleaned_data['time'],
            date=create_form.cleaned_data['date'],
            )
            database.save()


    context = {'create_form' : create_form, 'reservation_slots' : reservation_slots, 'restaurant_id':restaurant_id}
    return render(request, 'website/reservationSlot.html',context) # our front end html

# adds name, email, and phone to a reservation
def confirm_reservation(request,reservation_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        phone_str = str(phone)
        # prints error message if phone number is in the wrong format 
        if (len(phone_str) != 10):
            messages.error(request, 'Invalid phone number')
            return render(request, 'website/reservationConf.html')

        ReservationSlot.objects.filter(id=reservation_id).update(name=name)
        ReservationSlot.objects.filter(id=reservation_id).update(email=email)
        ReservationSlot.objects.filter(id=reservation_id).update(phone=phone)
        ReservationSlot.objects.filter(id=reservation_id).update(booked=True)
        reservation_slot = ReservationSlot.objects.all()

    else :
        reservation_slot = ReservationSlot.objects.all()

    context = {'reservation_slot' : reservation_slot}
    return render(request, 'website/reservationConf.html', context)


# Displaying the list of reservations and removing reservations
def reservation_list(request,restaurant_id):
    if request.method == 'GET' and 'date' in request.GET:
        date = request.GET.get('date')
        reservation_list = ReservationSlot.objects.filter(date=date, restaurant__pk=restaurant_id)
        return render(request, 'website/reservationList.html', {'reservation_list': reservation_list, 'mydate' : date, 'restaurant_id':restaurant_id})


    if request.method == 'GET' and 'id' in request.GET:
        id = request.GET.get('id')
        ReservationSlot.objects.filter(id=id,restaurant__pk=restaurant_id).delete()
        reservation_list = ReservationSlot.objects.filter(restaurant__pk=restaurant_id)
        return render(request, 'website/reservationList.html', {'reservation_list': reservation_list, 'restaurant_id':restaurant_id})

    else:
        return render(request, 'website/reservationList.html', {'restaurant_id':restaurant_id})

# Table
def table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    context = {'table' : table,'table_id' : table_id}
    return render(request, 'website/table.html', context)

# Creates a list of all current tables
def table_list(request, restaurant_id):
    table_list = Table.objects.filter(restaurant__pk=restaurant_id)
    context = {'table_list': table_list}
    return render(request, 'website/table_list.html', context)

# Creating a table for an order
def create_table(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    #order = get_object_or_404(Order, pk=order_id)
    #order_list = OrderItem.objects.filter(restaurant__pk=restaurant_id)
    #table_list = Table.objects.filter(order__pk=restaurant_id)
    if request.method == 'POST':
        form = CreateTableForm(request.POST)
        if form.is_valid():
            tab = Table.objects.create(
                table_number=form.cleaned_data['tablenumber'],
                #order_list = order_list,
                restaurant = restaurant
            )
            tab.save()
            url = '/website/order_summary/' + str(restaurant.id) + '/' # + str(restaurant.id)
            return HttpResponseRedirect(url)
    else:
        form = CreateTableForm()
        context = {'form': form, 'restaurant' : restaurant, }
    return render(request, 'website/create_table.html', context)

def close_table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    restaurant = table.restaurant
    if request.method == "POST":
        table.delete()
        url = '/website/table_list/' + str(restaurant.id) + '/'
        return redirect(url)

    context={'table' : table}
    return render(request, 'website/close_table.html', context)


