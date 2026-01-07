from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from access.models import AccessRule
from access.serializers import AccessRuleSerializer
from api.permissions import IsAdminUserPermission


class AccessRuleViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для админов для управления правилами доступа к бизнес-ресурсам.
    """
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    http_method_names = ['get', 'patch']
