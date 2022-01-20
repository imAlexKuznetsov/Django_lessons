from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS # для сообщений обо всей модели
from django.utils.deconstruct import deconstructible # для создания серилизации при миграци (мигр не раб с влож класс)


# create custom validator, only for example, joke
def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s - не чётное, эта доска для четных цен)))',
                              code='odd', params={'value': val})


# create custom validator class
@deconstructible  # позволяет провести миграцию несмотря на наличие вложенного класса
class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно быть в диапазоне от %(min)s до %(max)s',
                                  code='out_of_range',
                                  params={'min': self.min_value, 'max': self.max_value})


# Create your models here.
class Bd(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар',
                             validators=[validators.RegexValidator(
                                 regex='^.{4,}$',
                                 message='Название должно быть длинее 4 символов',
                             )])
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена',
                              validators=[validate_even, MinMaxValueValidator(10, 10000000)])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    def __str__(self):
        return  self.title

    def title_and_price(self):
        if self.price:
            return '%s (%.2f)' % (self.title, self.price)
        else:
            return self.title
    title_and_price.short_description = 'Название и цена'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']
        unique_together = ('title', 'published')

    # the whole model custom validations, for example content is not null and is not negatives
    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательные цены')
        if errors:
            errors[NON_FIELD_ERRORS] = ValidationError('Ни как не могу сохранить эти данные!')
            raise ValidationError(errors)


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class Measure(models.Model):
    class Measurement(float, models.Choices):
        METERS = 1.0, 'Метры'
        FEET = 0.3048, 'Футы'
        YARDS = 0.9144, 'Ярды'

    measurement = models.FloatField(choices=Measurement.choices)
