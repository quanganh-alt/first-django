from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .decorators import unauthenticated_user, allowed_users
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CreateUserForm, CustomerForm

from .filters import *
# Create your views here.


@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_orders = orders.count()
	total_customers = customers.count()

	delivered = orders.filter(status = 'Delivered').count()

	pending = orders.filter(status = 'Pending').count()
	context = {
		'orders': orders,
		'customers': customers,
		'total_orders': total_orders,
		'total_customers': total_customers,
		'delivered': delivered,
		'pending': pending
	}
	return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def customer(request,pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	total_orders = orders.count()
	myfilter = OrderFilter(request.GET, queryset=orders)
	orders = myfilter.qs
	context = {
		'customer': customer,
		'orders': orders,
		'total_orders': total_orders,
		'myfilter': myfilter
	}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
def create_order(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer': customer})
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context = {
		'formset': formset
	}
	return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		form.save()
		return redirect('/')
	context = {
		'form': form
	}
	return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {
		'item': order
	}
	return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request, 'Username or password is incorrect')
	return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')

@unauthenticated_user
def register(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	context = {
		'form': form
	}
	return render(request, 'accounts/register.html', context)

def userPage(request):
	orders = request.user.customer.order_set.all()
	customers = Customer.objects.all()

	total_orders = orders.count()
	total_customers = customers.count()

	delivered = orders.filter(status='Delivered').count()

	pending = orders.filter(status='Pending').count()
	context = {
		'orders': orders,
		'customers': customers,
		'total_orders': total_orders,
		'total_customers': total_customers,
		'delivered': delivered,
		'pending': pending
	}
	return render(request, 'accounts/user.html', context)


def account_setting(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
		return redirect('account')
	context = {
		'form': form
	}
	return render(request, 'accounts/account_setting.html', context)