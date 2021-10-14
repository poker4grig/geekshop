import os

from django.shortcuts import render

from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None, page_id=1):
    products = Product.objects.filter(category_id=category_id) if category_id is not None else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        product_paginator = paginator.page(page_id)
    except PageNotAnInteger as e:
        product_paginator = paginator.page(1)
    except EmptyPage as e:
        product_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'Каталог',
        'categorys': ProductCategory.objects.all(),
        'clear_categorys': '/products/',
        'products': product_paginator}
    return render(request, 'mainapp/products.html', context)
