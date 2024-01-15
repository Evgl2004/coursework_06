from django.urls import path
from main.views import (SendingListListView, SendingListCreateView, SendingListUpdateView, SendingListDetailView,
                        SendingListDeleteView, ClientsListView, ClientsCreateView, ClientsUpdateView, ClientsDetailView,
                        ClientsDeleteView)
from main.apps import MainConfig
from django.views.decorators.cache import cache_page

app_name = MainConfig.name


urlpatterns = [
    path('', SendingListListView.as_view(), name='home'),
    path('sending_lists/', SendingListListView.as_view(), name='list_sending_list'),
    path('sending_list/create/', SendingListCreateView.as_view(), name='create_sending_list'),
    path('sending_list/edit/<int:pk>/', SendingListUpdateView.as_view(), name='edit_sending_list'),
    path('sending_list/view/<int:pk>/', SendingListDetailView.as_view(), name='view_sending_list'),
    path('sending_list/delete/<int:pk>/', SendingListDeleteView.as_view(), name='delete_sending_list'),
    path('clients/', ClientsListView.as_view(), name='list_client'),
    path('client/create/', ClientsCreateView.as_view(), name='create_client'),
    path('client/edit/<int:pk>/', ClientsUpdateView.as_view(), name='edit_client'),
    path('client/view/<int:pk>/', ClientsDetailView.as_view(), name='view_client'),
    path('client/delete/<int:pk>/', ClientsDeleteView.as_view(), name='delete_client'),
]