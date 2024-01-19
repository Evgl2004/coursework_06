from django.db import models
from datetime import datetime

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(**NULLABLE, verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='изображение')
    data_publication = models.DateTimeField(default=datetime.now(), verbose_name='дата публикации')
    view_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

