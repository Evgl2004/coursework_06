from django.contrib import admin

from main.models import Clients, Mails, SendingLists, LogSendingMails


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'owner')
    list_filter = ('first_name', 'email', 'owner')
    search_fields = ('first_name', 'email', 'owner')


@admin.register(Mails)
class MailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'subject')
    list_filter = ('owner', )
    search_fields = ('owner', 'subject')


@admin.register(SendingLists)
class SendingListsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'data_begin', 'data_end', 'period')
    list_filter = ('owner', )
    search_fields = ('owner', )


@admin.register(LogSendingMails)
class LogSendingMailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client', 'data_send', 'is_done')
    list_filter = ('client', )
    search_fields = ('client', )
