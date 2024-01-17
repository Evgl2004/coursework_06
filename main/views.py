from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from main.models import Clients, Mails, SendingLists, LogSendingMails
from main.forms import ClientsForm, MailsForm, SendingListsFromUser, SendingListsFromModerator, LogSendingMailsForm
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from main.cron import change_status_sending_lists, checking_logs_and_send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
# from django.shortcuts import redirect, Http404
# from main.services import is_moderator


class HomeTemplateView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['total_sending_lists'] = SendingLists.objects.all().count()
        context['total_sending_lists_is_active'] = SendingLists.objects.filter(is_active=True).count()
        context['distinct_count_clients'] = Clients.objects.values('email').distinct().count()

        return context


class SendingListListView(LoginRequiredMixin, ListView):
    model = SendingLists
    form_class = SendingListsFromUser


class SendingListCreateView(LoginRequiredMixin, CreateView):
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
        checking_logs_and_send_mail()

        return super().form_valid(form)


class SendingListUpdateView(LoginRequiredMixin, UpdateView):
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


class SendingListDetailView(LoginRequiredMixin, DetailView):
    model = SendingLists


class SendingListDeleteView(LoginRequiredMixin, DeleteView):
    model = SendingLists
    success_url = reverse_lazy('main:home')


class ClientsListView(LoginRequiredMixin, ListView):
    model = Clients
    form_class = ClientsForm


class ClientsCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    form_class = ClientsForm
    success_url = reverse_lazy('main:list_client')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientsUpdateView(LoginRequiredMixin, UpdateView):
    model = Clients
    form_class = ClientsForm

    def get_success_url(self):
        return reverse('main:edit_client', args=[self.kwargs.get('pk')])


class ClientsDetailView(LoginRequiredMixin, DetailView):
    model = Clients


class ClientsDeleteView(LoginRequiredMixin, DeleteView):
    model = Clients
    success_url = reverse_lazy('main:list_client')

    permission_required = 'main.delete_sending_list'


class LogSendingMailListView(LoginRequiredMixin, ListView):
    model = LogSendingMails
    form_class = LogSendingMailsForm

