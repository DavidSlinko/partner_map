import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class LegalFace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='Наименование Юр лица')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='Наименование бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'


class Bonus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_bonus = models.CharField(max_length=200)
    name = models.CharField(max_length=255)
    image = models.URLField()
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Added field

    def __str__(self):
        return f"{self.id} - {self.name} - {self.value}"

    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'


class GeoData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100, verbose_name='Тип "АЗС, гипермаркет"')
    entity = models.ForeignKey(LegalFace, on_delete=models.CASCADE, verbose_name='Юридическое лицо',
                                   related_name='geo_data')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='geo_data')

    # entity = models.IntegerField()
    # brand = models.IntegerField()

    region = models.CharField(max_length=255)
    address = models.CharField(max_length=200, verbose_name='Адрес')
    nomenclature = models.CharField(max_length=100, blank=True, null=True, verbose_name='Номенклатура')
    discount = models.CharField(max_length=50, verbose_name='Скидка')
    nds = models.BooleanField(verbose_name='НДС')
    coordinates = models.CharField(max_length=200, verbose_name='Координаты')
    # logo_photo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name='Логотип')
    # logo_link = models.CharField(max_length=500, blank=True, null=True, verbose_name='Ссылка на лого')
    logo = models.CharField(max_length=255)
    status = models.BooleanField(verbose_name='Статус работы')
    bonuses = models.ManyToManyField(Bonus, related_name='geo_data', verbose_name='Бонусы')



    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Гео объект'
        verbose_name_plural = 'Гео объекты'
