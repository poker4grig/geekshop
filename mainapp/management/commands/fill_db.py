import os, json

from django.contrib.auth.models import AbstractUser
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from mainapp.models import ProductCategory, Product


JSON_PATH = 'mainapp/fixtures/'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name), mode='r', encoding='utf-8') as infile:

        return json.load(infile)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('category.json')

        ProductCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategory(**cat)
            new_category.save()

        products = load_from_json('product.json')

        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = ProductCategory.objects.get(id=category)
            prod['category'] = _category
            new_product = Product(**prod)
            new_product.save()

        super_user = User.objects.create_superuser('sergey', 'poker4grig@yandex.ru', '123')




