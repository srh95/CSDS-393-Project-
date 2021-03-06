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
    UpdateMenuItemForm,
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
            currentList = Order.objects.all()
            if(currentList.count() > 0):
                currentItem = Order.objects.all()[:1].get()
                restaurantID = currentItem.item_restaurant
            else:
                restaurantID = menu_item.restaurant_id
            if(restaurantID == menu_item.restaurant_id):
                for x in range(form.cleaned_data['num_items']):
                    print('create thingy here')
                    database = Order.objects.create(
                        item_name = menu_item.menu_item_name,
                        item_price = menu_item.menu_item_price,
                        item_number = tmpNum,
                        item_restaurant = menu_item.restaurant_id
                    )
                    database.save()
                    tmpNum = tmpNum+1
            url = '/website/restaurant/user/' + str(menu_item.restaurant_id)
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
    order_restaurant = 0
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
        order_restaurant = x.item_restaurant
    print(order_list_price)
    order_list_price = str(order_list_price)
    context = {'order_list': order_list, 'order_list_price': order_list_price, 'order_restaurant': order_restaurant}
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
            messages.error(request, 'Please insert a number value for price')
            url = '/website/restaurant/edit_menu/' + str(restaurant_id)
            return HttpResponseRedirect(url)
    else:
        form = AddMenuItemForm()
    return render(request, 'website/edit_menu.html', {'form' : form, 'menu_list' : menu_list, 'restaurant_id' : restaurant_id})

def edit_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    if request.method=='POST':
        form = UpdateMenuItemForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['menuitemname']:
                menu_item.menu_item_name = form.cleaned_data['menuitemname']
                menu_item.save(update_fields=['menu_item_name'])
            if form.cleaned_data['menuitemdescription']:
                menu_item.menu_item_description = form.cleaned_data['menuitemdescription']
                menu_item.save(update_fields=['menu_item_description'])
            if form.cleaned_data['menuitemprice']:
                menu_item.menu_item_price = form.cleaned_data['menuitemprice']
                menu_item.save(update_fields=['menu_item_price'])
            url = '/website/restaurant/edit_menu/' + str(menu_item.restaurant_id)
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Please insert a number value for price')
            url = '/website/restaurant/edit_menu_item/' + str(menu_item.id)
            return HttpResponseRedirect(url)
    else:
        form = UpdateMenuItemForm()
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
            try:
                if(Restaurant.objects.get(restaurant_name=form.cleaned_data['restaurantname'])):
                    messages.error(request, 'Restaurant already exists')
                    return HttpResponseRedirect('/website/accounts/register')
            except ObjectDoesNotExist:
                print('no restaurants yet')
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
    return render(request, 'website/register.html', {'form' : form})

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
    if request.method == 'GET' and 'date' in request.GET:
        date = request.GET.get('date')
        try:
            reservation_slots = ReservationSlot.objects.filter(date=date, restaurant__pk=restaurant_id)
            return render(request, 'website/reservation.html', {'reservation_slots': reservation_slots, 'mydate': date})
        except ValidationError:
            messages.error(request, 'Incorrect date format. The date must be entered in the format YYYY-MM-DD.')

    return render(request, 'website/reservation.html')




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

        else :
            messages.error(request, 'Make sure input is valid. (Table ID should be a one or two digit number. Number of people should be an number. Date should be a valid date in the format DD/MM/YYYY. Time should be a valid time entered in the format H:MM)')
            return render(request, 'website/reservationSlot.html')


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
        messages.error(request, 'Reservation successfully made')
        url = '/reservation_conf/' + str(reservation_id)
        return HttpResponseRedirect(url)
    else :
        reservation_slot = ReservationSlot.objects.all()
    reservation = ReservationSlot.objects.get(id=reservation_id)
    context = {'reservation_slot' : reservation_slot, 'restaurant_id' : reservation.restaurant_id}
    return render(request, 'website/reservationConf.html', context)


# Displaying the list of reservations and removing reservations
def reservation_list(request,restaurant_id):
    if request.method == 'GET' and 'date' in request.GET:
        date = request.GET.get('date')
        try:
            reservation_list = ReservationSlot.objects.filter(date=date, restaurant__pk=restaurant_id)
            return render(request, 'website/reservationList.html', {'reservation_list': reservation_list, 'mydate' : date, 'restaurant_id':restaurant_id})
        except ValidationError:
            messages.error(request, 'Incorrect date format. The date must be entered in the format YYYY-MM-DD.')


    if request.method == 'GET' and 'id' in request.GET:
        id = request.GET.get('id')
        try:
            ReservationSlot.objects.filter(id=id, restaurant__pk=restaurant_id).delete()
            reservation_list = ReservationSlot.objects.filter(restaurant__pk=restaurant_id)
            return render(request, 'website/reservationList.html', {'reservation_list': reservation_list, 'restaurant_id':restaurant_id})
        except ValueError:
            messages.error(request, 'Invalid reservation number. The reservation number must be a number.')
            return render(request, 'website/reservationList.html')

    else:
        context = {"restaurant_id" : restaurant_id}
        #reservation_list = ReservationSlot.objects.filter(restaurant__pk=restaurant_id)
        return render(request, 'website/reservationList.html', context)

# Table
def table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    context = {'table' : table,'table_id' : table_id, "restaurant_id" : table.restaurant_id}
    return render(request, 'website/table.html', context)

# Creates a list of all current tables
def table_list(request, restaurant_id):
    table_list = Table.objects.filter(restaurant__pk=restaurant_id)
    context = {'table_list': table_list, 'restaurant_id' : restaurant_id}
    return render(request, 'website/table_list.html', context)

# Creating a table for an order
def create_table(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    #order = get_object_or_404(Order, pk=order_id)
    #order_list = OrderItem.objects.filter(restaurant__pk=restaurant_id)
    #table_list = Table.objects.filter(order__pk=restaurant_id)
    order_list = Order.objects.all()
    order_str = ""
    for x in order_list:
        order_str = order_str + x.item_name + ', '
    if request.method == 'POST':
        form = CreateTableForm(request.POST)
        if form.is_valid():
            #try
                tab = Table.objects.create(
                    table_number=form.cleaned_data['tablenumber'],
                    #order_list = order_list,
                    restaurant = restaurant,
                    table_order = order_str
                )
                tab.save()
                url = '/website/order_summary/' # + str(restaurant.id)
                return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Please insert a number value for table number')
            url = '/website/create_table/' + str(restaurant_id) + "/"
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

    context={'table' : table, 'restaurant' : restaurant}
    return render(request, 'website/close_table.html', context)


