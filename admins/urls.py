"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import index, UserUpdateView, UserListView, UserCreateView, UserDeleteView, CategoryListView, \
    CategoriesCreateView, CategoriesUpdateView, CategoriesDeleteView

app_name = 'admins'
urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),

    path('categories/', CategoryListView.as_view(), name='admins_categories'),
    path('categories-create/', CategoriesCreateView.as_view(), name='admins_categories_create'),
    path('categories-update/<int:pk>/', CategoriesUpdateView.as_view(), name='admins_categories_update'),
    path('categories-delete/<int:pk>/', CategoriesDeleteView.as_view(), name='admins_categories_delete'),

    # path('categories-create/', admins_categories_create, name='categories_create'),
    # path('categories-update/<int:pk>/', admins_categories_update, name='categories_update'),
    # path('categories/delete/<int:pk>/', admins_categories_delete, name='categories_delete'),

]
