'''store Views configuration

In this file there are renders for different views
used in application.
'''

from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import cartData, guestOrder

import json
import datetime

# Store view
def store(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

# Cart view
def cart(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

# Checkout view
def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# Item detail view
def itemView(request, id):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/item.html', context)

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
        
    else:
        customer, order = guestOrder(request, data)
            
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
    
    return JsonResponse('Payment complete!', safe=False)
