from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, CustomDispatchMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from users.models import User


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Geekshop | Авторизация'
    success_url = reverse_lazy('index')

    # success_url = 'http://127.0.0.1:8000/'

    def get(self, request, *args, **kwargs):
        sup = super(LoginListView, self).get(request, *args, **kwargs)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
            # return HttpResponseRedirect(self.success_url)
        return sup


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
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request,
                                 'Поздравляем, вы успешно зарегистрировались! Письмо с активацией было отправлено '
                                 'вам на почту')
            return redirect(self.success_url)
        return redirect(self.success_url)

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Для активации учетной записи {user.username} перейдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале перейдите по ссылке: \n ' \
                  f'{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    @staticmethod
    def verify(request, email, activation_key):
        try:
            # user = User.objects.get(email=email)
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_created = None
                user.is_active = True
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))


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
    #
    # комментируем get_context_data, т.к. есть контекстный процессор
    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        form_edit = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and form_edit.is_valid():
            # form_edit.save()
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
