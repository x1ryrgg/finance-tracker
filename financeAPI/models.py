from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
import os


class User(AbstractUser):
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    avatar = models.ImageField(blank=True, null=True, upload_to='media/photo', verbose_name="Фотография")


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name="Ник", related_name="profile")
    all_money = models.FloatField(max_length=1000000000000, blank=True, default=0, verbose_name="Баланс")
    text = models.TextField(blank=True, default="Пусто", verbose_name="Пожелания")
    image = models.ImageField(upload_to='photo', verbose_name="Фото", blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    obj = models.ManyToManyField('Objective', blank=True, verbose_name="Цели", related_name="objs")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

        ordering = ['time_create']

    def __str__(self):
        return f"{self.user} | {self.all_money}"


class Objective(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    object = models.CharField(max_length=100, db_index=True, verbose_name="Название цели")
    obj_money = models.FloatField(max_length=1000000000000, null=False, db_index=True ,verbose_name='Сумма для цели')
    slug = models.SlugField(max_length=255, unique=True, blank=False)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

        ordering = ['id']

    def __str__(self):
        return f"{self.object} | {self.obj_money}"

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_name = unidecode(self.object)
            self.slug = slugify(transliterated_name)
        return super(Objective, self).save(*args, **kwargs)


"""
функция срабатывает каждый раз, когда выполняется сохранение в модели Objective.
sender - это отправитель, из какой модели идет сохранение.
profile - экземпляр модели Profile связанный с пользователем который создал объект Objective.
Далее в поле obj модели profile добавляется только что созданный объект Objective.
Метод add для поля ManyToManyField позволяет добавлять один или несколько объектов, которые вы хотите связать с профилем.
"""
@receiver(post_save, sender=Objective)
def add_objective_to_profile(sender, instance, created, **kwargs):
    if created:
        try:
            profile = Profile.objects.get(user=instance.user)
            profile.obj.add(instance)  # Добавляем только что созданный Objective в obj профиля
        except Profile.DoesNotExist:
            pass


