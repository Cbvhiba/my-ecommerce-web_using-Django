from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email, send_forget_password_mail
from products.models import ColorVariant, Coupon, Product, SizeVariant

# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

    class Meta:
        verbose_name_plural = '1 . Profiles'

    def __str__(self) -> str:
        return self.user.first_name

    def get_cart_count(self):
        return cartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()

@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
            print('/////////',email_token,'///////')
    except Exception as e:
        print(e)


class UserDetails(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=150)
    address = models.TextField()
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)

    
class cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = '2 . Carts'

    def __str__(self) -> str:
        return self.user

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        Price = []
        for cart_item in cart_items:
            print("**",cart_item)
            print("////////////")
            print(cart_item.product)
            print("////////////")

            # Price.append(cart_item.product.price)

            if cart_item.product.discount:
                discounted_price = cart_item.product.price - cart_item.product.price * cart_item.product.discount_percent / 100
                Price.append(discounted_price)
                print('*****************')
                print('discount price = ', discounted_price)
                print('*****************')

            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.price
                Price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                Price.append(size_variant_price)

        if self.coupon:
            if self.coupon.min_amount < sum(Price):
                return sum(Price) - self.coupon.discount_price

        print(Price)
        return sum(Price)


class cartItems(BaseModel):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = '3 . CartItems'

    def __str__(self) -> str:
        return self.product.product_name
    

    def get_product_price(self):
        Price = []

        if self.product.discount:
            discounted_price = self.product.price - self.product.price * self.product.discount_percent / 100
            Price.append(discounted_price)
            print('*****************')
            print('discount price = ', discounted_price)
            print('*****************')

        if self.color_variant:
            color_variant_price = self.color_variant.price
            Price.append(color_variant_price)
        if self.size_variant:
            size_variant_price = self.size_variant.price
            Price.append(size_variant_price)

        print(Price)
        return sum(Price)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    address = models.TextField()
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    total_price = models.IntegerField()
    payment_mode = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    orderStatus = (
        ('Pending','Pending'),
        ('Shipped','Shipped'),
        ('Out for delivery','Out for delivery'),
        ('Arrived','Arrived')
    )
    status = models.CharField(max_length=150, choices=orderStatus, default='Pending')
    message = models.TextField(null=True, blank=True)
    tracking_no = models.CharField(max_length=150, null=True, blank=True)

    # razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    # razorpay_patment_id = models.CharField(max_length=200, null=True, blank=True)
    # razorpay_signature = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.first_name)


class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.product.product_name

    def get_product_price(self):
        Price = []

        if self.product.discount:
            discounted_price = self.product.price - self.product.price * self.product.discount_percent / 100
            Price.append(discounted_price)
            print('*****************')
            print('discount price = ', discounted_price)
            print('*****************')

        print(Price)
        return sum(Price)


# @receiver(post_save, sender=User)
# def send_forget_password_token(sender, instance, created, **kwargs):
#     try:
#         if created:
#             forget_password_token = str(uuid.uuid4())
#             print(forget_password_token)
#             Profile.objects.create(user=instance, forget_password_token=forget_password_token)
#             email = instance.email
#             send_forget_password_mail(email, forget_password_token)

#     except Exception as e:
#         print(e)