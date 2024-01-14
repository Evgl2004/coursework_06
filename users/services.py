from django.core.mail import send_mail
from django.urls import reverse_lazy
from config import settings


def send_welcome_mail(new_user):
    send_mail(
        subject='Поздравляем с регистрацией!',
        message=f'Вы зарегистрировалась на нашей платформе!\n'
                f'Добро пожаловать!\n'
                f'Активация профиля: {reverse_lazy("users:activate", args=[new_user.code])}\n',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[new_user.email]
    )