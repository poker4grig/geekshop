from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from mainapp.models import ProductCategory, Product
from users.models import User


# class TestMainSmokeTest(TestCase):
#     status_code_success = 200
#     status_code_render = 302
#     username = 'django'
#     email = 'django@mail.ru'
#     password = 'geekbrains'
#
#     new_user_data = {
#         'user_name': 'django1',
#         'first_name': 'Django',
#         'last_name': 'Django2',
#         'password1': '!Zxcvbn123456',
#         'password2': '!Zxcvbn123456',
#         'email': 'djang111o@mail.ru',
#     }
#
#     def setUp(self) -> None:
#         self.user = User.objects.create_superuser(username=self.username, email=self.email, password=self.password)
#         self.client = Client()
#
#     def test_login(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, self.status_code_success)
#
#         self.assertTrue(response.context['user'].is_anonymous)
#
#         self.client.login(username=self.username, password=self.password)
#         response = self.client.get('/users/login/')
#         self.assertEqual(response.status_code, self.status_code_render)
#
#     def test_register(self):
#         response = self.client.post('/users/register/', data=self.new_user_data)
#         self.assertEqual(response.status_code, self.status_code_render)
#         new_user = User.objects.get(username=self.new_user_data['user_name'])
#         print(new_user)
#
#         activation_url = f"{settings.DOMAIN_NAME}/users/verify/{self.new_user_data['email']}/{new_user.activation_key}/"
#         response = self.client.get(activation_url)
#         self.assertEqual(response.status_code, self.status_code_success)
#
#         new_user.refresh_from_db()
#         self.assertTrue(new_user.is_active)
#
#     def tearDown(self) -> None:
#         pass
# ==============================================================================================


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = User.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')

        self.user = User.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains')

        self.user_with__first_name = User.objects.create_user('umaturman', 'umaturman@geekshop.local', 'geekbrains',
                                                              first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'users', 'ordersapp', 'baskets')


class TestUserManagement(TestCase):

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username='tarantino', password='geekbrains')

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def test_user_logout(self):
        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
