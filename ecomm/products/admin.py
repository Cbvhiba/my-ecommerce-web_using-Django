from django.contrib import admin
from products.models import *
# Register your models here.


admin.site.register(Coupon)
admin.site.register(Tag)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['catogary_name', 'image_tag']
admin.site.register(Catogary, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory', 'image_tag']
admin.site.register(SubCategory, SubcategoryAdmin)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'is_featured']
    list_editable = ['is_featured']
    inlines = [ProductImageAdmin]

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price', 'color_bg']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size', 'price']
    model = SizeVariant

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImages)