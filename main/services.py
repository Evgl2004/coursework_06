from smtplib import SMTPException

from main.models import Mails, LogSendingMails
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail


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