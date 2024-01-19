from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.apps import BlogsConfig
from blogs.views import BlogListView

app_name = BlogsConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='list'),
]