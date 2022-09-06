from django.shortcuts import render
from products.models import Product, ProductReview, SizeVariant, ColorVariant
from accounts.forms import ReviewForm

# Create your views here.


def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        related_product = Product.objects.filter(catogary=product.catogary).exclude(slug=slug)[:4]
        product_review = ProductReview.objects.filter(product__slug=slug)

        context = {'product': product, 'related_product': related_product, 'product_review': product_review}

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)

        return render(request, 'product/product.html', context=context)

    except Exception as e:
        print(e)

    return render(request, 'product/product.html')