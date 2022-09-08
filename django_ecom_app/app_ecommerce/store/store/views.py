'''store Views configuration

In this file there are renders for different views
used in application.
'''

from django.shortcuts import render
from django.http import JsonResponse
from .models import *

import json
import datetime

# Store view
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # This is used to display the amount of items near the cart icon
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

# Cart view
def cart(request):
    if request.user.is_authenticated:
        # First, let's assign logged user to the Customer value
        customer = request.user.customer
        # Second, let's check if the order we'are looking for is already created
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # The next line gets all the Order Items child from the specific Order parent object
        items = order.orderitem_set.all()
        # The reason why we are adding this here is to render the amount of items in every template
        cartItems = order.get_cart_items
    else:
        try:
            # The request.COOKIES part gets items from unauthenticated users' carts
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart:', cart)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        
        # This loop will get the items from the session and update cartItems
        for i in cart:
            cartItems += cart[i]['quantity']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

# Checkout view
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# Update item view
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('Product ID:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    # This line checks if the order item exists based on the order and product
    # If it exists, it doesn't need to create a new one - it needs to change the quantity of it
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

# Process order view
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                street = data['shipping']['street'],
                city = data['shipping']['city'],
                voivodeship = data['shipping']['voivodeship'],
                zipcode = data['shipping']['zipcode'],
            )
        
    else:
        print('User is not logged in.')
    
    return JsonResponse('Payment complete!', safe=False)

