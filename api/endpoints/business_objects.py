from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import BusinessResourcePermission
from business_objects.models import BusinessObject
from business_objects.serializers import (
    BusinessObjectReadSerializer,
    BusinessObjectUpdateSerializer,
    BusinessObjectWriteSerializer,
)


class BusinessObjectViewSet(viewsets.ModelViewSet):
    """CRUD для бизнес-объектов конкретного ресурса."""
    serializer_class = BusinessObjectReadSerializer
    permission_classes = [IsAuthenticated, BusinessResourcePermission]
    http_method_names = ['get', 'post', 'patch', 'delete']
    resource_name = None

    def get_serializer_class(self):
        if self.action == 'create':
            return BusinessObjectWriteSerializer
        if self.action == 'partial_update':
            return BusinessObjectUpdateSerializer
        return BusinessObjectReadSerializer

    def get_queryset(self):
        # Query-параметр "resource" нужен только для list
        if self.action == 'list':
            resource_name = self.request.query_params.get('resource')
            if not resource_name:
                return BusinessObject.objects.none()
            return BusinessObject.objects.filter(resource__name=resource_name)

        return BusinessObject.objects.all()

    def perform_create(self, serializer):
        # Сохраняем владельца при создании объекта
        serializer.save(owner=self.request.user)
