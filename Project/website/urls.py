from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login, name='login'),
    path('restaurant/menu_list/<int:menu_item_id>/', views.menu_item, name='menuitem'),
    path('restaurant/menu_list/', views.menu_list, name='menulist'),
    path('restaurant/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    path('restaurant/edit_menu/<int:restaurant_id>/', views.edit_menu, name='editmenu'),
    path('restaurant/', views.restaurant_list, name='restaurants'),
    path('search/', views.search, name='search')
]
