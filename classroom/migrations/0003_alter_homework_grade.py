# Generated by Django 3.2.9 on 2022-01-14 04:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_auto_20220104_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='grade',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
    ]
