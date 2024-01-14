# Generated by Django 5.0.1 on 2024-01-13 18:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='logsendingmails',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.clients', verbose_name='клиент'),
        ),
        migrations.AddField(
            model_name='mails',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='sendinglists',
            name='clients',
            field=models.ManyToManyField(to='main.clients', verbose_name='клиенты'),
        ),
        migrations.AddField(
            model_name='sendinglists',
            name='mail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mails', verbose_name='письмо'),
        ),
        migrations.AddField(
            model_name='sendinglists',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='logsendingmails',
            name='send_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sendinglists', verbose_name='рассылка'),
        ),
    ]
