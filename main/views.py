from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from main.models import Clients, Mails, SendingLists, LogSendingMails
from main.forms import ClientsForm, MailsForm, SendingListsFromUser, SendingListsFromModerator, LogSendingMailsForm
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from main.cron import change_status_sending_lists
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
# from django.shortcuts import redirect, Http404
# from main.services import is_moderator


class SendingListListView(ListView):
    model = SendingLists
    form_class = SendingListsFromUser


class SendingListCreateView(CreateView):
    model = SendingLists
    form_class = SendingListsFromUser
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        MailFormset = inlineformset_factory(SendingLists, Mails, extra=1, form=MailsForm)

        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST)
        else:
            context_data['formset'] = MailFormset()

        return context_data

    def form_valid(self, form):

        formset = self.get_context_data()['formset']

        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            attachments = formset.save(commit=False)
            for attachment in attachments:
                attachment.owner = self.request.user
                attachment.save()

        change_status_sending_lists()

        return super().form_valid(form)


class SendingListUpdateView(UpdateView):
    model = SendingLists
    form_class = SendingListsFromUser

    def get_success_url(self):
        return reverse('main:edit_sending_list', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(SendingLists, Mails, form=MailsForm, extra=1)
        if self.request.method == 'POST':
            formset = MailFormset(self.request.POST, instance=self.object)
        else:
            formset = MailFormset(instance=self.object)

        context_data['formset'] = formset

        change_status_sending_lists()

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class SendingListDetailView(DetailView):
    model = SendingLists


class SendingListDeleteView(DeleteView):
    model = SendingLists
    success_url = reverse_lazy('main:home')


class ClientsListView(ListView):
    model = Clients
    form_class = ClientsForm


class ClientsCreateView(CreateView):
    model = Clients
    form_class = ClientsForm
    success_url = reverse_lazy('main:list_client')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientsUpdateView(UpdateView):
    model = Clients
    form_class = ClientsForm

    def get_success_url(self):
        return reverse('main:edit_client', args=[self.kwargs.get('pk')])


class ClientsDetailView(DetailView):
    model = Clients


class ClientsDeleteView(DeleteView):
    model = Clients
    success_url = reverse_lazy('main:list_client')

    permission_required = 'main.delete_sending_list'


class LogSendingMailListView(ListView):
    model = LogSendingMails
    form_class = LogSendingMailsForm

