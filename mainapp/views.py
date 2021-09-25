from django.shortcuts import render
import os

from mainapp.models import ProductCategory, Product
import json

MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


# с json
def products(request):
    context = {
        'title': 'geekshop',
        'category': ProductCategory.objects.all(),
        'products': Product.objects.all()}
    return render(request, 'mainapp/products.html', context)
