from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
# from .forms import RegisterForm
# from .forms import EditMenuForm
# from .forms import LoginForm
from django.core.exceptions import ValidationError
from .models import (
    Table,
)
from website.models import Restaurant

from django.views.generic import ListView, DetailView, View
from django.utils import timezone

def index(request):
    return HttpResponse("Hello, world. You're at the currentTables index.")

def table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    context = {'table' : table, 'table_id' : table_id}
    return render(request, 'website/table.html', context)