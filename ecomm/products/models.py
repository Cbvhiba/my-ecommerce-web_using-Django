from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from base.models import *
from django.utils.text import slugify
from django.utils.html import mark_safe

# Create your models here.


class Catogary(BaseModel):
    catogary_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catogary_img = models.ImageField(upload_to='catogaries')

    class Meta:
        verbose_name_plural = '1 . Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.catogary_img.url))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.catogary_name)
        super(Catogary, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.catogary_name


class SubCategory(BaseModel):
    subcategory = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catogary = models.ForeignKey(Catogary, on_delete=models.CASCADE, related_name='subcategory')
    subcategory_img = models.ImageField(upload_to='subcategory')

    class Meta:
        verbose_name_plural = '2 . Subcategories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.subcategory_img.url))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subcategory)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.subcategory  


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = '5 . ColorVariants'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background:%s"></div>' % (self.color_name))

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = '6 . SizeVariants'

    def __str__(self) -> str:
        return self.size


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '7 . Tags'

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catogary = models.ForeignKey(Catogary, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    discount_percent = models.FloatField(default=0)
    total_quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=250, null=True, blank=True)
    product_desc = models.TextField()
    product_information = models.TextField(null=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL,null=True, blank=True)
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '3 . Products'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def discount(self):
        if self.discount_percent > 0:
            discounted_price = self.price - self.price * self.discount_percent / 100
            return discounted_price


    def __str__(self) -> str:
        return self.product_name

    def get_product_price_by_size(self, size):
        return self.price + SizeVariant.objects.get(size=size).price

class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products')

    class Meta:
        verbose_name_plural = '4 . ProductImages'

    def __str__(self) -> str:
        return self.product.product_name


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    min_amount = models.IntegerField(default=800)

    class Meta:
        verbose_name_plural = '8 . Coupons'

    def __str__(self) -> str:
        return self.coupon_code