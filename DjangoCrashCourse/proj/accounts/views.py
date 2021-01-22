from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
 
# Create your views here.

@login_required(login_url='login')
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


def registerPage(request):
    form = CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            return redirect('login')
    
    context ={'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):

    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context ={}
    return render(request, 'accounts/login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html', {'products': products})


@login_required(login_url='login')
def customer(request, slug):
    customer = Customer.objects.get(id=slug)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'orders': orders,
        'customer': customer,
        'order_count': order_count,
        'myfilter': myFilter
    }
    
    return render(request,'accounts/customer.html', context)


@login_required(login_url='login')
def CreateOrder(request, slug):
    OrderFormSet = inlineformset_factory(Customer, Order, fields =('product', 'status', 'note'), extra=10)
    customer= Customer.objects.get(id=slug)
    formset = OrderFormSet(queryset=Order.objects.none(),instance = customer)
    context ={'formset': formset}
    if request.method=="POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid:
            formset.save()
            return redirect('/')
    return render(request,'accounts/order_form.html', context)


@login_required(login_url='login')
def UpdateOrder(request, slug):
    OrderFormSet = inlineformset_factory(Customer, Order, fields =('product', 'status', 'note'), extra=0)
    order = Order.objects.get(id=slug)
    formset = OrderFormSet(instance = order.customer)

    if request.method=="POST":
        formset = OrderFormSet(request.POST, instance = order.customer)
        if formset.is_valid:
            formset.save()
            print(request.POST)
            return redirect('/')

    context = {'formset': formset}

    return render(request,'accounts/order_form.html', context)


@login_required(login_url='login')
def DeleteOrder(request, slug):
    order = Order.objects.get(id=slug)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
