from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from access.models import Role, RoleEnum
from api.permissions import IsAdminUserPermission, IsSelfOrAdmin
from users.models import User
from users.serializers import (
    UserCreateSerializer,
    UserReadSerializer,
    UserRoleUpdateSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ('list', 'update_role'):
            # Для смены роли: только аутентифицированный админ
            return [IsAuthenticated(), IsAdminUserPermission()]
        # Остальные действия только со своими профилями
        return [IsAuthenticated(), IsSelfOrAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        if self.action == 'update_role':
            # Для смены роли: только аутентифицированный админ
            return UserRoleUpdateSerializer
        return UserReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Устанавливаем роль "User" по умолчанию
        user.role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Деактивация пользователя вместо полного удаления."""
        user = self.get_object()
        user.is_active = False
        user.save()

        # Если передан refresh токен, добавляем его в blacklist
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['patch'],
        url_path='update-role',
        url_name='update_role'
    )
    def update_role(self, request, pk=None):
        """Смена роли пользователя (только для админа)."""
        user = self.get_object()

        serializer = self.get_serializer(
            user,  # Передаем объект для обновления
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        # Возвращаем данные обновленного пользователя
        return Response(serializer.data)
