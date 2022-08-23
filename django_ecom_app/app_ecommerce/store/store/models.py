from django.db import models
from django.contrib.auth.models import User


# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    # 'digital' field tells us essentially if the product needs to be shipped 
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    # This property function is assuring us that if the Product doesn't have an image
    # attached to it, the page will still load and not throw an error
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
# Order Model
class Order(models.Model):
    # 'customer' field is here so that Customer can have multiple orders
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # If this field is set to False, we can keep adding items to the order but if this changes
    # to True, it means that this order is completed. Next items will be added to the new order
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
# OrderItem Model
# This model creates Item objects that need to be added to Cart with Many-To-One relationship
# In this model the 'order' field is our cart and the OrderItem object is an item within the cart
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # The child of an Order object
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
# ShippingAddress Model
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    voivodeship = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.street