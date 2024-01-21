from django.urls import path
from main.views import (SendingListListView, SendingListCreateView, SendingListUpdateView, SendingListDetailView,
                        SendingListDeleteView, ClientsListView, ClientsCreateView, ClientsUpdateView,
                        ClientsDeleteView, LogSendingMailListView, HomeTemplateView,
                        toggle_activity)
from main.apps import MainConfig
from django.views.decorators.cache import cache_page

app_name = MainConfig.name


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('sending_lists/', SendingListListView.as_view(), name='list_sending_list'),
    path('sending_list/create/', SendingListCreateView.as_view(), name='create_sending_list'),
    path('sending_list/edit/<int:pk>/', SendingListUpdateView.as_view(), name='edit_sending_list'),
    path('sending_list/view/<int:pk>/', cache_page(60)(SendingListDetailView.as_view()), name='view_sending_list'),
    path('sending_list/delete/<int:pk>/', SendingListDeleteView.as_view(), name='delete_sending_list'),
    path('clients/', ClientsListView.as_view(), name='list_client'),
    path('client/create/', ClientsCreateView.as_view(), name='create_client'),
    path('client/edit/<int:pk>/', ClientsUpdateView.as_view(), name='edit_client'),
    path('client/delete/<int:pk>/', ClientsDeleteView.as_view(), name='delete_client'),
    path('log_sending_mail/', LogSendingMailListView.as_view(), name='list_log_sending_mail'),
    path('toggle_activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]