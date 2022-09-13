'''store Utilities configuration

In this file there are utility methods
used in the store app e.g. these following
the D.R.Y. (Don't Repeat Yourself) concept
'''

import json
from .models import *

# cookieCart function contains all the logic that are used for operating user's cart
def cookieCart(request):
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
        # But first let's use try/except method to prevent querying non existing items
        try:
            cartItems += cart[i]['quantity']
            
            # Now we can update the number of items in car and its total price in the cart view
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                # 'digital':product.digital,
                'get_total':total,
            }
            
            items.append(item)
            
            if(product.digital == False):
                order['shipping'] = True
                
        except:
            pass
    
    return {'cartItems': cartItems, 'order': order, 'items': items}
        
        
# cartData function handles all the logic for cart regarding authenticated and unauthenticated users
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    return {'cartItems': cartItems, 'order': order, 'items': items}

# guestOrder function handles orders processing made by an unauthenticated users
def guestOrder(request, data):
    print('User is not logged in.')
        
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    # Accessing the cookie data that is dictionary representation of what database would look like
    # This data contains information about order of unauthenticated users
    cookieData = cookieCart(request)
    
    items = cookieData['items']
    
    # By using get_or_create() method, we are able to attach existing email address to the unlogged
    # customer and check how many times this user shopped at the store despite having no account
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    # Attaching name from cookies to unauthorized user
    # This is done outside get_or_create() method in case user decides to change their name
    customer.name = name
    customer.save()
    
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    
    # Now we need to loop through the items set in line 114 and add them to the database, create them
    # and attach them to the order item
    for item in items:
        # Accessing the product's id from the Product model
        product = Product.objects.get(id=item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product=product,            # values from OrderItem model; product is that id we got
            order=order,                # order is the object we created above
            quantity=item['quantity'],  # quantity is from item set in the utils file
        )
    
    return customer, order