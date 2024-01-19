from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, Http404

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView,  ListView

from users.models import User
from users.forms import UserRegisterForm, UserFormFromUser, UserFormFromModerator

from main.services import is_moderator

from django.contrib.auth.decorators import login_required, permission_required

from uuid import uuid4

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
        new_user.auth_guid_code = str(uuid4())
        new_user.is_active = False

        new_user.save()

        send_welcome_mail(new_user)

        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserFormFromUser

    def get_success_url(self):
        return reverse('users:profile', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        if is_moderator(self.request.user) and self.object != self.request.user:
            return UserFormFromModerator
        else:
            return UserFormFromUser

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object == self.request.user or is_moderator(self.request.user) or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404("Доступ только для владельца")


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    form_class = UserFormFromUser

    permission_required = 'users.set_active'

    def get_queryset(self):
        return super().get_queryset().order_by('pk')


def activate_code(request, code):
    user = get_object_or_404(User, auth_guid_code=code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


@login_required
@permission_required('users.set_active')
def toggle_activity(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()

    return redirect(reverse('users:list'))