from django.contrib import admin
from accounts.models import Order, OrderItems, Profile, UserDetails, cart, cartItems
# Register your models here.

admin.site.register(Profile)

admin.site.register(UserDetails)

admin.site.register(cart)

admin.site.register(cartItems)

admin.site.register(Order)

admin.site.register(OrderItems)