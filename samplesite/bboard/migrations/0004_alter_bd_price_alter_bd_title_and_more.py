# Generated by Django 4.0.1 on 2022-01-17 13:40

import bboard.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0003_rubric_alter_bd_options_alter_bd_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bd',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[bboard.models.validate_even, bboard.models.MinMaxValueValidator(10, 10000000)], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='bd',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Название должно быть длинее 4 символов', regex='^.{4,}$')], verbose_name='Товар'),
        ),
        migrations.AlterUniqueTogether(
            name='bd',
            unique_together={('title', 'published')},
        ),
    ]
