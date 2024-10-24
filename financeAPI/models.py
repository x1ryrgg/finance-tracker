from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class User(AbstractUser):
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    avatar = models.ImageField(blank=True, null=True, upload_to='media/photo', verbose_name="Фотография")


class Profile(models.Model):
    name = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name="Ник")
    all_money = models.FloatField(max_length=1000000000000, blank=True, default=0, verbose_name="Баланс")
    text = models.TextField(blank=True, default="Пусто", verbose_name="Пожелания")
    obj = models.ForeignKey('Objective', on_delete=models.CASCADE, default='Нет целей',
                                blank=True, verbose_name="Цели")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f"{self.name} | {self.all_money}"


class Objective(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=None ,verbose_name="Пользователь")
    object = models.CharField(max_length=100, db_index=True, verbose_name="Название цели")
    obj_money = models.FloatField(max_length=1000000000000, default=0, verbose_name='Сумма для цели', db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=False)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.object} | {self.obj_money}"

    def get_absolute_url(self):
        return reverse('object_update', kwargs={'object_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_name = unidecode(self.object)
            self.slug = slugify(transliterated_name)
        return super(Objective, self).save(*args, **kwargs)


