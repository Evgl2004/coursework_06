from django.urls import path
from users.apps import UsersConfig
from users.views import (UserLoginView, UserLogoutView, RegisterView, UserUpdateView, UserListView,
                         activate_code, toggle_activity)

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='list'),
    path('activate_code/<str:code>', activate_code, name='activate_code'),
    path('toggle_activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]