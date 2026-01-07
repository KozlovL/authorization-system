from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from access.models import Role
from access.serializers import RoleSerializer
from users.models import User


class UserReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения данных пользователя."""

    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'role',
        )
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
        )

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Пароли не совпадают'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        return UserReadSerializer(instance).data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
        )

    def to_representation(self, instance):
        return UserReadSerializer(instance).data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор токена с проверкой is_active."""

    @classmethod
    def get_token(cls, user):
        if not user.is_active:
            raise serializers.ValidationError('Пользователь деактивирован.')
        return super().get_token(user)


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для смены роли пользователя (только админ)."""
    role = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Role.objects.all()
    )

    class Meta:
        model = User
        fields = (
            'role',
        )

    def update(self, instance, validated_data):
        """Обновление роли пользователя."""
        role = validated_data.get('role')

        instance.role = role
        instance.save()

        return instance

    def to_representation(self, instance):
        """Возвращаем представление пользователя после обновления."""
        return UserReadSerializer(instance).data
