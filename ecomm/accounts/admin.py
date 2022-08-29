from django.contrib import admin
from accounts.models import Profile, cart, cartItems
# Register your models here.

admin.site.register(Profile)

admin.site.register(cart)

admin.site.register(cartItems)