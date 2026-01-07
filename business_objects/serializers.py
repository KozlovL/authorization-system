from rest_framework import serializers

from business_objects.models import BusinessObject, BusinessResource
from users.serializers import UserReadSerializer


class BusinessResourceSerializer(serializers.ModelSerializer):
    """Сериализатор для бизнес-ресурса."""
    class Meta:
        model = BusinessResource
        fields = (
            'id',
            'name',
            'description',
        )


class BusinessObjectReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения бизнес-объекта."""
    owner = UserReadSerializer(read_only=True)
    resource = BusinessResourceSerializer(read_only=True)

    class Meta:
        model = BusinessObject
        fields = (
            'id',
            'name',
            'description',
            'resource',
            'owner',
        )


class BusinessObjectWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания бизнес-объекта."""
    resource = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BusinessResource.objects.all()
    )

    class Meta:
        model = BusinessObject
        fields = (
            'name',
            'description',
            'resource'
        )

    def to_representation(self, instance):
        return BusinessObjectReadSerializer(instance).data


class BusinessObjectUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления бизнес-объекта."""

    class Meta:
        model = BusinessObject
        fields = (
            'name',
            'description',
        )

    def to_representation(self, instance):
        return BusinessObjectReadSerializer(instance).data
