from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from baskets.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Geekshop - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем, вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Geekshop - Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, 'Поздравляем, профиль сохранен!')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, 'Профиль не сохранен!')

    total_quantity = 0
    total_summ = 0
    baskets = Basket.objects.filter(user=request.user)
    for basket in baskets:
        total_quantity += basket.quantity
        total_summ += basket.summ()

    context = {
        'title': 'Geekshop - Профайл',
        'form': UserProfileForm(instance=request.user),
        'baskets': Basket.objects.filter(user=request.user),
        'total_quantity': total_quantity,
        'total_summ': total_summ
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
