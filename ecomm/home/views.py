from django.shortcuts import render
from products.models import Product, Catogary
# Create your views here.


def index(request):
    catogaries = Catogary.objects.all()[:4]
    products = Product.objects.filter(is_featured=True)[:8]
    context = {'products': products, 'catogaries': catogaries}
    return render(request, 'home/home.html', context)