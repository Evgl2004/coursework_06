from smtplib import SMTPException

from main.models import Mails, LogSendingMails, SendingLists, Clients
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail

from django.core.cache import cache


def send_mail_for_send_list(send_list, client_list=None):

    if client_list is None:
        client_list = send_list.clients.all()

    select_mails = Mails.objects.filter(send_list=send_list)

    if select_mails.exists():
        for mail in select_mails:
            for client in client_list:
                try:
                    result = send_mail(
                        subject=mail.subject,
                        message=mail.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )

                    log_list = LogSendingMails.objects.create(
                        data_send=datetime.now(),
                        is_done=result,
                        error_massage='',
                        send_list=send_list,
                        client=client
                    )

                    log_list.save()

                except SMTPException as error:

                    log_list = LogSendingMails.objects.create(
                        data_send=datetime.now(),
                        is_done=False,
                        error_massage=error,
                        send_list=send_list,
                        client=client
                    )

                    log_list.save()


def is_moderator(user):
    return user.groups.filter(name='moderator').exists()


def get_cache_total_sending_lists():
    if settings.CACHE_ENABLED:
        key = 'total_sending_lists'
        total_sending_lists = cache.get(key)
        if total_sending_lists is None:
            total_sending_lists = SendingLists.objects.all().count()
            cache.set(key, total_sending_lists)
    else:
        total_sending_lists = SendingLists.objects.all().count()
    return total_sending_lists


def get_cache_total_sending_lists_is_active():
    key = 'total_sending_lists_is_active'
    total_sending_lists_is_active = cache.get(key)
    if total_sending_lists_is_active is None:
        total_sending_lists_is_active = SendingLists.objects.filter(is_active=True).count()
        cache.set(key, total_sending_lists_is_active)
    else:
        total_sending_lists_is_active = SendingLists.objects.filter(is_active=True).count()
    return total_sending_lists_is_active


def get_cache_distinct_count_clients():
    key = 'distinct_count_clients'
    distinct_count_clients = cache.get(key)
    if distinct_count_clients is None:
        distinct_count_clients = Clients.objects.values('email').distinct().count()
        cache.set(key, distinct_count_clients)
    else:
        distinct_count_clients = Clients.objects.values('email').distinct().count()
    return distinct_count_clients


