from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
 
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

def customer(request, slug):
    customer = Customer.objects.get(id=slug)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {
        'orders': orders,
        'customer': customer,
        'order_count': order_count
    }
    print(context)
    return render(request,'accounts/customer.html', context)

def CreateOrder(request, slug):
    OrderFormSet = inlineformset_factory(Customer, Order, fields =('product', 'status'), extra=10)
    customer= Customer.objects.get(id=slug)
    formset = OrderFormSet(queryset=Order.objects.none(),instance = customer)
    context ={'formset': formset}
    if request.method=="POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid:
            formset.save()
            return redirect('/')
    return render(request,'accounts/order_form.html', context)

def UpdateOrder(request, slug):
    order = Order.objects.get(id=slug)
    form = OrderForm(instance=order)

    if request.method=="POST":
        form = OrderForm(request.POST, instance = order)
        if form.is_valid:
            form.save()
            print(request.POST)
            return redirect('/')
    context = {'form': form}

    return render(request,'accounts/order_form.html', context)

def DeleteOrder(request, slug):
    order = Order.objects.get(id=slug)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
