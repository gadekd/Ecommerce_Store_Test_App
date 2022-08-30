'''store Views configuration

In this file there are renders for different views
used in application.
'''

from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Store render
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

# Cart render
def cart(request):
    if request.user.is_authenticated:
        # First, let's assign logged user to the Customer value
        customer = request.user.customer
        # Second, let's check if the order we'are looking for is already created
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # The next line gets all the Order Items child from the specific Order parent object
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

# Checkout render
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

# Update item render
def updateItem(request):
    return JsonResponse('Item was added', safe=False)

