from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView

from users.models import User
from users.forms import UserRegisterForm, UserForm

import uuid

from django.contrib.auth.mixins import LoginRequiredMixin

from users.services import send_welcome_mail


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.code = str(uuid.uuid4())
        new_user.is_active = False

        new_user.save()

        send_welcome_mail(new_user)

        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def activate_code(code):
    user = get_object_or_404(User, code=code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
