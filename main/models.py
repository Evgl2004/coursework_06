from django.db import models
from datetime import datetime

from django.conf import settings

NULLABLE = {'null': True, 'blank': True}


class Clients(models.Model):

    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.EmailField(unique=True, verbose_name='почта')
    comment = models.CharField(max_length=250, verbose_name='комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class SendingLists(models.Model):

    PERIOD_DAY = 'day'
    PERIOD_WEEK = 'week'
    PERIOD_MONTH = 'month'

    PERIODS = (
        (PERIOD_DAY, 'раз в день'),
        (PERIOD_WEEK, 'раз в неделю'),
        (PERIOD_MONTH, 'раз в месяц')
    )

    STATUS_CREATE = 'create'
    STATUS_START = 'start'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATE, 'создан'),
        (STATUS_START, 'запущен'),
        (STATUS_DONE, 'завершен')
    )

    data_begin = models.DateTimeField(default=datetime.now, verbose_name='дата начала')
    data_end = models.DateTimeField(default=datetime.now, verbose_name='дата конца')
    period = models.CharField(max_length=5, default='day', choices=PERIODS, verbose_name='период')
    status = models.CharField(max_length=7, default='create', choices=STATUSES, verbose_name='статус')

    clients = models.ManyToManyField(Clients, verbose_name='клиенты')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    is_active = models.BooleanField(default=True, verbose_name='активна')

    class Meta:
        verbose_name = 'список рассылки'
        verbose_name_plural = 'списки рассылок'

        permissions = [
            (
                'set_active_sending_list',
                'Возможно отключить рассылку'
            )
        ]

    def __str__(self):
        return f'{self.owner} {self.data_begin} {self.data_end} {self.period} {self.status}'


class Mails(models.Model):

    subject = models.CharField(max_length=150, verbose_name='тема')
    body = models.TextField(verbose_name='тело')

    send_list = models.ForeignKey(SendingLists, on_delete=models.CASCADE, **NULLABLE, verbose_name='рассылка')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'

    def __str__(self):
        return f'{self.owner} {self.subject}'


class LogSendingMails(models.Model):

    data_send = models.DateTimeField(default=datetime.now, verbose_name='дата')
    is_done = models.BooleanField(default=True, verbose_name='статус')
    error_massage = models.CharField(max_length=150, verbose_name='ошибка', **NULLABLE)

    client = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='клиент')
    send_list = models.ForeignKey(SendingLists, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'журнал рассылки'
        verbose_name_plural = 'журналы рассылок'

    def __str__(self):
        return f'{self.is_done} {self.client} {self.data_send}'
