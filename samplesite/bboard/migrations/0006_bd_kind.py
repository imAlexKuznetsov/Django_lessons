# Generated by Django 4.0.1 on 2022-01-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0005_measure_alter_bd_rubric_advuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='bd',
            name='kind',
            field=models.CharField(blank=True, choices=[(None, 'Выберите тип публикуемого объявления'), ('b', 'Куплю'), ('s', 'Продам'), ('c', 'Обменяю')], max_length=1),
        ),
    ]
