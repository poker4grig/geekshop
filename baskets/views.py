from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from geekshop.mixin import UserDispatchMixin
from mainapp.models import Product, ProductCategory

from baskets.models import Basket
# Create your views here.


class BasketCreateView(CreateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'mainapp/products.html'
    success_url = reverse_lazy('products:index')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'product_id' in kwargs:
            product_id = kwargs['product_id']
            if product_id:
                product = Product.objects.get(id=product_id)
                baskets = Basket.objects.filter(user=request.user, product=product)
                if not baskets.exists():
                    Basket.objects.create(user=request.user, product=product, quantity=1)
                else:
                    basket = baskets.first()
                    basket.quantity += 1
                    basket.save()

        return redirect(self.success_url)


class BasketDeleteView(DeleteView, UserDispatchMixin):
    model = Basket
    success_url = reverse_lazy('users:profile')


class BasketUpdateView(UpdateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    pk_url_kwarg = 'basket_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BasketUpdateView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        super(BasketUpdateView, self).get(request, *args, **kwargs)
        if request.is_ajax():
            basket_id = kwargs[self.pk_url_kwarg]
            quantity = kwargs['quantity']
            baskets = Basket.objects.filter(id=basket_id)
            if baskets.exists():
                basket = baskets.first()
                if quantity > 0:
                    basket.quantity = quantity
                    basket.save()
                else:
                    basket.delete()

            result = render_to_string('baskets/baskets.html', self.get_context_data(*args, **kwargs), request=request)

            return JsonResponse({'result': result})

        return redirect(self.success_url)


# @login_required
# def basket_add(request, product_id):
#     user_select = request.user
#     product = Product.objects.get(id=product_id)
#     baskets = Basket.objects.filter(user=user_select, product=product)
#     if not baskets.exists():
#         Basket.objects.create(user=user_select, product=product, quantity=1)
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#
# @login_required
# def basket_remove(request, product_id):
#     Basket.objects.get(id=product_id).delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#
# @login_required
# def basket_edit(request, id, quantity):
#     if request.is_ajax():
#         basket = Basket.objects.get(id=id)
#         if quantity > 0:
#             basket.quantity = quantity
#             basket.save()
#         else:
#             basket.delete()
#
#         baskets = Basket.objects.filter(user=request.user)
#         context = {
#             'baskets': baskets,
#         }
#         result = render_to_string('baskets/baskets.html', context)
#         return JsonResponse({'result': result})
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





