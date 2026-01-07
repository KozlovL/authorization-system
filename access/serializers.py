from rest_framework import serializers

from access.models import AccessRule, Role, RoleEnum
from business_objects.models import BusinessResource, BusinessResourceEnum


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли пользователя."""

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
        )


class AccessRuleSerializer(serializers.ModelSerializer):
    """Сериализатор для управления правилами доступа ролей к ресурсам."""
    role = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Role.objects.all()
    )
    business_resource = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BusinessResource.objects.all()
    )

    class Meta:
        model = AccessRule
        fields = (
            'id',
            'role',
            'business_resource',
            'read_owned_permission',
            'read_all_permission',
            'create_permission',
            'update_owned_permission',
            'update_all_permission',
            'delete_owned_permission',
            'delete_all_permission',
        )

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
