from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products),
    path('customer/<int:pk_test>', views.customer, name='customer'),
    path('create_order/<int:pk>', views.create_order,name='create_order'),
    path('update_order/<str:pk>', views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder,name='delete_order'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user'),
    path('account/', views.account_setting, name='account')
]