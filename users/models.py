from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models

from users.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH, USERNAME_STR_WIDTH


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        unique=True,
        max_length=NAME_MAX_LENGTH,
        validators=[
            UnicodeUsernameValidator,
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
            )
        ],
        verbose_name='Никнейм'
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH
    )
    email = models.EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        verbose_name='Почта'
    )
    role = models.ForeignKey(
        'access.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ('username',)
        default_related_name = 'users'

    def __str__(self):
        return self.username[:USERNAME_STR_WIDTH]
