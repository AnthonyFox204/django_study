from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from . forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
import DjangoProjectTest.settings as settings


#LoginUser#Start####################################################################################
def login_user(request: HttpRequest):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('home')
    else:
        form = LoginUserForm()

    data = {
        'form': form,
    }

    return render(request, 'users/login.html', context=data)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }

    # def get_success_url(self):
    #     return reverse_lazy('home')
#LoginUser#End######################################################################################


#LogoutUser#Start###################################################################################
def logout_user(request: HttpRequest):
    logout(request)
    return redirect('users:login')
#LogoutUser#End#####################################################################################


#RegisterUser#Start#################################################################################
def register_user(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()

    data = {
        'form': form,
    }

    return render(request, 'users/register.html', context=data)


class RegisterUser(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    extra_context = {
        'title': 'Регистрация',
    }
    success_url = reverse_lazy('users:login')
#RegisterUser#End###################################################################################


#ProfileUser#Start##################################################################################
class ProfileUser(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileUserForm
    extra_context = {
        'title': 'Профиль пользователя',
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')
#ProfileUser#End####################################################################################


#UserPasswordChange#Start###########################################################################
class UserPasswordChange(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {
        'title': 'Изменение пароля',
    }
#UserPasswordChange#End#############################################################################
