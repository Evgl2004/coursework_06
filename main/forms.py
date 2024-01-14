from django import forms
from main.models import Clients, Mails, SendingLists, LogSendingMails


class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        exclude = 'owner'


class MailsForm(forms.ModelForm):
    class Meta:
        model = Mails
        exclude = 'owner'


class SendingListsFromUser(forms.ModelForm):
    class Meta:
        model = SendingLists
        fields = ('data_begin', 'data_end', 'period', 'status', 'clients')


class SendingListsFromModerator(forms.ModelForm):
    class Meta:
        model = SendingLists
        fields = ('status',)


class LogSendingMailsForm(forms.ModelForm):
    class Meta:
        model = LogSendingMails
        fields = '__all__'
