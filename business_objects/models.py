from django.conf import settings
from django.db import models

from business_objects.constants import NAME_MAX_LENGTH, NAME_STR_WIDTH


class BusinessResourceEnum(models.TextChoices):
    PRODUCTS = 'products', 'Товары'
    ORDERS = 'orders', 'Заказы'
    SHOPS = 'shops', 'Магазины'


class BusinessResource(models.Model):
    """Модель бизнес-ресурса."""
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        choices=BusinessResourceEnum.choices
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        default_related_name = 'business_resources'

    def __str__(self):
        return self.name[:NAME_STR_WIDTH]


class BusinessObject(models.Model):
    """Модель бизнес-объекта."""

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    description = models.TextField(blank=True)
    resource = models.ForeignKey(
        BusinessResource,
        on_delete=models.CASCADE,
        related_name='business_objects'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_objects'
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'business_objects'

    def __str__(self):
        return self.name[:NAME_STR_WIDTH]
