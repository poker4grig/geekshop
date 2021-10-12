from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Geekshop | Авторизация'
    success_url = reverse_lazy('index')


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 messages.success(request, f'Поздравляем {user.username}, вы успешно вошли в свой профиль!')
#                 return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Geekshop - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Geekshop | Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем, вы успешно зарегистрировались!')
            return redirect(self.success_url)
        return redirect(self.success_url)


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop | Профайл'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    # @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    # def dispatch(self, request, *args, **kwargs):
    #     return super(ProfileFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем, профиль сохранен!')
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             messages.error(request, form.errors)
#
#     context = {
#         'title': 'Geekshop - Профайл',
#         'form': UserProfileForm(instance=request.user),
#         'baskets': Basket.objects.filter(user=request.user)
#     }
#     return render(request, 'users/profile.html', context)


class LogoutListView(LogoutView):
    template_name = 'mainapp/index.html'


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
