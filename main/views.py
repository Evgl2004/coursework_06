from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from main.models import Clients, Mails, SendingLists, LogSendingMails
from main.forms import ClientsForm, MailsForm, SendingListsFromUser, SendingListsFromModerator, LogSendingMailsForm
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, Http404
from main.services import is_moderator


class SendingListListView(ListView):
    model = SendingLists
    form_class = SendingListsFromUser


class SendingListCreateView(CreateView):
    model = SendingLists
    form_class = SendingListsFromUser
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class SendingListUpdateView(UpdateView):
    model = SendingLists
    form_class = SendingListsFromUser

    def get_success_url(self):
        return reverse('main:edit_product', args=[self.kwargs.get('pk')])


class SendingListDetailView(DetailView):
    model = SendingLists


class SendingListDeleteView(DeleteView):
    model = SendingLists
    success_url = reverse_lazy('main:home')

    permission_required = 'main.delete_product'

