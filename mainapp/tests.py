from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from mainapp.models import Product, ProductCategory


# class TestMainSmokeTest(TestCase):
#     status_code_success = 200
#
#     # 1 предустановленные параметры
#     def setUp(self) -> None:
#         category = ProductCategory.objects.create(name='Test')
#         Product.objects.create(category=category, name='product_test', price=100)
#         Product.objects.create(category=category, name='product_test2', price=50)
#
#         self.client = Client()
#
#     # 2 выполнение теста
#     def test_products_pages(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, self.status_code_success)
#
#     def test_products_product(self):
#         for product_item in Product.objects.all():
#             response = self.client.get(f'/products/detail/{product_item.pk}/')
#             self.assertEqual(response.status_code, self.status_code_success)
#
#     def test_products_profile(self):
#         response = self.client.get('/users/profile/')
#         self.assertEqual(response.status_code, 302)
#
#     # 3 освобождение памяти от данных
#
#     def tearDown(self) -> None:
#         pass

class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        # print(dir(response))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'users', 'ordersapp', 'baskets')

