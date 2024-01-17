from main.models import SendingLists, LogSendingMails
from datetime import datetime, timedelta
from main.services import send_mail_for_send_list


def change_status_sending_lists():
    select_send_lists = SendingLists.objects.filter(status=SendingLists.STATUS_CREATE)
    if select_send_lists.exists():
        for send_list in select_send_lists:
            if datetime.now() >= send_list.data_begin.replace(tzinfo=None):
                send_list.status = SendingLists.STATUS_START
                send_list.save()

    select_send_lists = SendingLists.objects.filter(status=SendingLists.STATUS_START)
    if select_send_lists.exists():
        for send_list in select_send_lists:
            if datetime.now() >= send_list.data_end.replace(tzinfo=None):
                send_list.status = SendingLists.STATUS_DONE
                send_list.save()


def checking_logs_and_send_mail():
    select_send_lists = SendingLists.objects.filter(status=SendingLists.STATUS_START)
    if select_send_lists.exists():
        for send_list in select_send_lists:
            select_log_lists = LogSendingMails.objects.filter(send_list=send_list)

            if select_log_lists.exists():
                for client in send_list.clients.all():
                    log = select_log_lists.filter(client=client).order_by("-data_send")[0]

                    if ((send_list.period == SendingLists.PERIOD_DAY
                         and datetime.now() >= (log.data_send + timedelta(days=1)).replace(tzinfo=None))
                            or
                        (send_list.period == SendingLists.PERIOD_WEEK
                         and datetime.now() >= (log.data_send + timedelta(days=7)).replace(tzinfo=None))
                            or
                         (send_list.period == SendingLists.PERIOD_MONTH
                          and datetime.now() >= (log.data_send + timedelta(days=30)).replace(tzinfo=None))):

                        send_mail_for_send_list(send_list, [client])
            else:
                send_mail_for_send_list(send_list)
