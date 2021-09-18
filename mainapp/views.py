from django.shortcuts import render
import os
import json

MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


# с json
def products(request):
    file_path = os.path.join(MODULE_DIR, 'fixtures/db.json')
    context = {
        'title': 'geekshop',
        'products': json.load(open(file_path, encoding='utf-8'))}
    return render(request, 'mainapp/products.html', context)

# без json
# def products(request):
#     context = {
#         'title': 'geekshop',
#         'products': [
#             {'name': 'Черный рюкзак Nike Heritage',
#              'price': '2 340,00 руб.',
#              'description': 'Плотная ткань. Легкий материал.',
#              'picture': 'Black-Nike-Heritage-backpack.png'},
#             {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
#              'price': '13 590,00 руб.',
#              'description': 'Гладкий кожаный верх. Натуральный материал.',
#              'picture': 'Black-Dr-Martens-shoes.png'},
#             {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
#              'price': '2 890,00 руб.',
#              'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.',
#              'picture': 'Dark-blue-wide-leg-ASOs-DESIGN-trousers.png'},
#             {'name': 'Худи черного цвета с монограммами adidas Originals',
#              'price': '6 090,00 руб.',
#              'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.',
#              'picture': 'Adidas-hoodie.png'},
#             {'name': 'Синяя куртка The North Face',
#              'price': '23 725,00 руб.',
#              'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.',
#              'picture': 'Blue-jacket-The-North-Face.png'},
#             {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
#              'price': '3 390,00 руб.',
#              'description': 'Материал с плюшевой текстурой. Удобный и мягкий.',
#              'picture': 'Brown-sports-oversized-top-ASOS-DESIGN.png'},
#         ]
#     }
#     return render(request, 'mainapp/products.html', context)


def test(request):
    context = {
        'title': 'geekshop',
        'header': 'Добро пожаловать на сайт',
        'user': 'Сергей',
        'date': 'Дата',
        'products': [
            {'name': 'Черный рюкзак Nike Heritage', 'price': '2 340,00 руб.'},
            {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': '13 590,00 руб.'},
            {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price': '2 890,00 руб.'},
            {'name': 'Худи черного цвета с монограммами adidas Originals', 'price': '6 090,00 руб.'},
            {'name': 'Синяя куртка The North Face', 'price': '23 725,00 руб.'},
            {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390,00 руб.'},
        ],
        'products_sale': [
            {'name': 'Красный шарф Adidas', 'price': '1 000,00 руб.'},
            {'name': 'Белый классический костюм HugoBoss', 'price': '2 000,00 руб.'},
        ]
    }
    return render(request, 'mainapp/test.html', context)

