from django.urls import path, include

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login, name='login'),
    path('restaurant/menu_list/<int:menu_item_id>/', views.menu_item, name='menuitem'),
    path('restaurant/menu_list/', views.menu_list, name='menulist'),
    path('restaurant/<int:restaurant_id>/', views.restaurant, name='restaurant'),
    path('restaurant/user/<int:restaurant_id>/', views.restaurant_user_side, name='restaurant_user_side'),
    path('restaurant/edit_menu/<int:restaurant_id>/', views.add_menu_item, name='addmenuitem'),
    path('restaurant/edit_menu_item/<int:menu_item_id>/', views.edit_menu_item, name='editmenuitem'),
    path('restaurant/delete_menu_item/<int:menu_item_id>', views.delete_menu_item, name='deletemenuitem'),
    path('restaurant/', views.search, name='restaurants'),
    path('search/', views.search, name='search'),
    path('order_summary/', views.order_list, name='order_list'),
    path('add_to_cart', views.add_to_cart, name = 'add-to-cart'),
    path('reserve_table/<int:restaurant_id>/', views.reserve_table, name='reserve_table'),
    path('create_reservation/<int:restaurant_id>/', views.create_reservation, name='create_reservation'),
    path('reservation_list/<int:restaurant_id>/', views.reservation_list, name='reservation_list'),
    path('reservation_conf/<int:reservation_id>/',views.confirm_reservation, name = 'confirm_reservation'),
    path('successPage/', views.paymentSuccess, name = 'successPage'),
    
]
