from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from geekshop.mixin import UserDispatchMixin
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache


# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


def get_link_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related('category')
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


class ProductListView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('mainapp:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categorys'] = get_links_category()

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        self.request.session['category_id'] = category_id

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        # products = Product.objects.filter(
        #     category_id=category_id).select_related(
        #     'category') if category_id is not None else Product.objects.all().select_related('category')
        products = get_link_product()
        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, category_id=None, page_id=1):
#     products = Product.objects.filter(category_id=category_id) if category_id is not None else Product.objects.all()
#
# paginator = Paginator(products, per_page=3)
# try:
#     product_paginator = paginator.page(page_id)
# except PageNotAnInteger as e:
#     product_paginator = paginator.page(1)
# except EmptyPage as e:
#     product_paginator = paginator.page(paginator.num_pages)
#
#     context = {
#         'title': 'Каталог',
#         'categorys': ProductCategory.objects.all(),
#         'products': product_paginator}
#     return render(request, 'mainapp/products.html', context)
