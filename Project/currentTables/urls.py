from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/<int:table_id>/', views.table, name='table'),
]
