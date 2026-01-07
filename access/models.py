from django.db import models

from access.constants import NAME_MAX_LENGTH, NAME_STR_WIDTH


class RoleEnum(models.TextChoices):
    """Названия ролей пользователей."""
    ADMIN = 'Admin', 'Администратор'
    MANAGER = 'Manager', 'Менеджер'
    USER = 'User', 'Пользователь'


class Role(models.Model):
    """Модель роли пользователя."""
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        choices=RoleEnum.choices,
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'roles'

    def __str__(self):
        return self.name[:NAME_STR_WIDTH]


class AccessRule(models.Model):
    """Модель правил доступа ролей к бизнес-ресурсам."""

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    business_resource = models.ForeignKey(
        'business_objects.BusinessResource',
        on_delete=models.CASCADE,
        related_name='rules'
    )

    read_owned_permission = models.BooleanField(default=True)
    read_all_permission = models.BooleanField(default=False)

    create_permission = models.BooleanField(default=False)

    update_owned_permission = models.BooleanField(default=True)
    update_all_permission = models.BooleanField(default=False)

    delete_owned_permission = models.BooleanField(default=True)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'business_resource'],
                name='unique_role_business_resource'
            )
        ]

    def __str__(self):
        return f'{self.role} → {self.business_resource.name}'
