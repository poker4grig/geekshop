from django.db import models

from mainapp.models import Product
from users.models import User
# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def summ(self):
        return self.quantity * self.product.price

    def total_summ(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.summ() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    # @staticmethod
    # def total_summ(user):
    #     baskets = Basket.objects.filter(user=user)
    #     return sum(basket.summ() for basket in baskets)
    #
    # @staticmethod
    # def total_quantity(user):
    #     baskets = Basket.objects.filter(user=user)
    #     return sum(basket.quantity for basket in baskets)

