from django.views.generic import ListView

from blogs.models import Blog
from blogs.forms import BlogForm


class BlogListView(ListView):
    model = Blog
    form_class = BlogForm