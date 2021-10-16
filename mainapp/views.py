from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from geekshop.mixin import UserDispatchMixin
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


class ProductListView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('mainapp:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categorys'] = ProductCategory.objects.all()

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        self.request.session['category_id'] = category_id

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        products = Product.objects.filter(
            category_id=category_id) if category_id is not None else Product.objects.all().order_by('id')

        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

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
