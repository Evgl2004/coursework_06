# Generated by Django 5.0.1 on 2024-01-13 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('comment', models.CharField(blank=True, max_length=250, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='LogSendingMails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_send', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата')),
                ('is_done', models.BooleanField(default=True, verbose_name='статус')),
                ('error_massage', models.CharField(blank=True, max_length=150, null=True, verbose_name='ошибка')),
            ],
            options={
                'verbose_name': 'журнал рассылки',
                'verbose_name_plural': 'журналы рассылок',
            },
        ),
        migrations.CreateModel(
            name='Mails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150, verbose_name='тема')),
                ('body', models.TextField(verbose_name='тело')),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
            },
        ),
        migrations.CreateModel(
            name='SendingLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_begin', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата начала')),
                ('data_end', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата конца')),
                ('period', models.CharField(choices=[('day', 'раз в день'), ('week', 'раз в неделю'), ('month', 'раз в месяц')], default='day', max_length=5, verbose_name='период')),
                ('status', models.CharField(choices=[('create', 'создан'), ('start', 'запущен'), ('done', 'завершен')], default='create', max_length=7, verbose_name='статус')),
            ],
            options={
                'verbose_name': 'список рассылки',
                'verbose_name_plural': 'списки рассылок',
            },
        ),
    ]
