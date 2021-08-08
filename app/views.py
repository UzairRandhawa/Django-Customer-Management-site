from . models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse, response
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
import json
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from . utils import cookieCart,cartData,guestORder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializer import TaksSerializer
from . models import Task
def main(request):
    context = {}
    return render(request, 'app/main.html', context)

def store(request):
    cartDat = cartData(request)
    cartitem = cartDat['cartitem']
    order = cartDat['order']
    items = cartDat['items']
    products = Product.objects.all()
    context = {'products': products, 'cartitem': cartitem,'shipping': False}
    return render(request, 'app/store.html', context)

def checkout(request):
    
    cartDat = cartData(request)
    cartitem = cartDat['cartitem']
    order = cartDat['order']
    items = cartDat['items']

    context = {'items':items,'order':order,'cartitem': cartitem}
    return render(request, 'app/checkout.html', context)

def cart(request):
    cartDat = cartData(request)
    cartitem = cartDat['cartitem']
    order = cartDat['order']
    items = cartDat['items']
    context = {'items':items,'order':order,'cartitem': cartitem}
    return render(request, 'app/cart.html', context)

# Create your views here.
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('Product:',productId)

    customer=request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp(),
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete = False)
        
    else:
        customer, order = guestORder(request,data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShipingAddress.objects.create(
            customer = customer,
            order = order,
            addrees = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
    )

    return JsonResponse('Payment Subbmitted', safe=False)

def logoutpage(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect ('store')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username and Password does not matched.')
    context = {}
    return render(request, 'app/loginn.html', context)

def registerpage(request):
    if request.user.is_authenticated:
        return redirect ('store')
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save() 
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account Registered Succesfully for ' + user)
            return redirect('login')
            print('Data successfully..')

    context = {'form':form}
    return render(request, 'app/register.html', context)
    
@api_view(['GET'])
def apioverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/'
    }


    return Response(api_urls)

@api_view(['GET'])
def tasklist(request):
    tasks=Task.objects.all()
    serializer = TaksSerializer(tasks, many = True)
    return Response(serializer.data)
