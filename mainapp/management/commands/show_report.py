from prettytable import PrettyTable
from datetime import timedelta

from django.core.management.base import BaseCommand
from ordersapp.models import OrderItem
from mainapp.models import Product
from django.db import connection
from django.db.models import F, Q, When, Case, IntegerField, DecimalField
from admins.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_timedelta = timedelta(hours=12)
        action_2_timedelta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__update__lte=F('order__created') + action_1_timedelta)
        action_2_condition = Q(order__update__gt=F('order__created') + action_1_timedelta) & Q(
            order__update__lte=F('order__created') + action_2_timedelta)
        action_3_condition = Q(order__update__gt=F('order__created') + action_2_timedelta)

        action_1_order = When(action_1_condition, then=ACTION_1)
        action_2_order = When(action_2_condition, then=ACTION_2)
        action_3_order = When(action_3_condition, then=ACTION_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * -action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        total_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        t_list = PrettyTable(['Заказ', 'Товар', 'Скидка', 'Время'])
        t_list.align = 'l'
        for orderitem in total_orders:
            t_list.add_row([f'{orderitem.action_order} заказ № {orderitem.pk}', f'{orderitem.product.name:15}',
                            f'{abs(orderitem.total_price):6.2f} руб.',
                            orderitem.order.update - orderitem.order.created])
        print(t_list)

