# Generated by Django 5.1.2 on 2024-11-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAPI', '0005_rename_obj_profile_objs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='objs',
        ),
        migrations.AddField(
            model_name='profile',
            name='obj',
            field=models.ManyToManyField(blank=True, default=0, related_name='objs', to='financeAPI.objective', verbose_name='Цели'),
        ),
    ]
