from django import forms
from main.models import Clients, Mails, SendingLists, LogSendingMails
from django.forms import DateTimeInput


class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ('owner',)


class MailsForm(forms.ModelForm):
    class Meta:
        model = Mails
        exclude = ('owner',)


class SendingListsFromUser(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        user = self.request.user

        super().__init__(*args, **kwargs)

        self.fields['clients'].queryset = Clients.objects.filter(owner=user)

    class Meta:
        model = SendingLists
        fields = ('data_begin', 'data_end', 'period', 'clients', )


class SendingListsFromModerator(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = SendingLists
        fields = ('is_active',)


class LogSendingMailsForm(forms.ModelForm):
    class Meta:
        model = LogSendingMails
        fields = '__all__'
