from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()
    context = {
        'customers': customers,
        'orders': orders,
        'pending': pending,
        'delivered': delivered,
        'total_orders': total_orders
    }
    return render(request,'accounts/home.html', context)

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html', {'products': products})

def customer(request):
    return render(request,'accounts/customer.html')