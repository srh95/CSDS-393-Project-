from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem
from django.template import loader

def index(request):
    return HttpResponse("Hello, world. You're at the website index.")

def menu_item(request, name):
    return HttpResponse("You're looking at menu item %s." % name)

def menu_list(request):
    menu_list = MenuItem.objects.all()
    context = {'menu_list': menu_list,}
    return render(request, 'website/menu_list.html', context)