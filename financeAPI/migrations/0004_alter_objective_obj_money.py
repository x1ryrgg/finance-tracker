# Generated by Django 5.1.2 on 2024-10-18 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeAPI', '0003_remove_profile_money_objective_obj_money_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='obj_money',
            field=models.FloatField(db_index=True, default=0, max_length=1000000000000, verbose_name='Сумма для цели'),
        ),
    ]