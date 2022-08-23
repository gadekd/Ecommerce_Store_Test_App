'''store Views configuration

In this file there are renders for different views
used in application.
'''

from django.shortcuts import render
from .models import *

# Store render
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

# Cart render
def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

# Checkout render
def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

