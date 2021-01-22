from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<slug:slug>', views.customer, name="customer"),
    path('create_order/<slug:slug>', views.CreateOrder, name="create_order"),
    path('update_order/<slug:slug>', views.UpdateOrder, name="update_order"),
    path('delete_order/<slug:slug>', views.DeleteOrder, name="delete_order"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

]