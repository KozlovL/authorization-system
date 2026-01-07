from rest_framework.permissions import BasePermission

from access.models import AccessRule, RoleEnum


class BusinessResourcePermission(BasePermission):
    """
    Пермишен для проверки прав доступа к бизнес-ресурсам.

    Логика:

    - Для каждой action (list, retrieve, create, partial_update, destroy)
      есть две гранулы прав: *_all_permission и *_owned_permission.
      Например, для partial_update:
        - update_all_permission: разрешает обновлять любые объекты
        - update_owned_permission: разрешает обновлять только свои объекты

    - Если *_all_permission = True → можно работать с любым объектом
    - Если *_all_permission = False и *_owned_permission = True
      → можно работать только с объектами, где obj.owner == request.user
    - Если обе False → доступ запрещён
    """

    # Соответствие действий view -> атрибуты AccessRule
    action_permission_map = {
        'list': ('read_all_permission', 'read_owned_permission'),
        'retrieve': ('read_all_permission', 'read_owned_permission'),
        'create': ('create_permission', None),
        'partial_update': ('update_all_permission', 'update_owned_permission'),
        'destroy': ('delete_all_permission', 'delete_owned_permission'),
    }

    def get_rule(self, *, user, resource_name):
        """Получить AccessRule или None."""
        if not user.is_authenticated or not resource_name:
            return None

        try:
            return AccessRule.objects.get(
                role=user.role,
                business_resource__name=resource_name
            )
        except AccessRule.DoesNotExist:
            return None

    def has_permission(self, request, view):
        action = view.action
        # Получаем имя правила доступа
        perm_all, _ = self.action_permission_map.get(action, (None, None))
        if perm_all is None:
            return False

        if view.action == 'list':
            # Получаем имя бизнес-ресурса
            resource_name = request.query_params.get('resource')
            if not resource_name:
                return False

            # Получаем правило доступа из БД
            rule = self.get_rule(
                user=request.user,
                resource_name=resource_name
            )

            return bool(rule and getattr(rule, perm_all, False))

        if view.action == 'create':
            # Получаем имя бизнес-ресурса
            resource_name = request.data.get('resource')
            if not resource_name:
                return False

            # Получаем правило доступа
            rule = self.get_rule(
                user=request.user,
                resource_name=resource_name
            )

            return bool(rule and getattr(rule, perm_all, False))

        return True

    def has_object_permission(self, request, view, obj):
        # Получаем имя правила доступа
        perm_all, perm_owned = self.action_permission_map.get(view.action, (None, None))
        if perm_all is None:
            return False

        # Получаем правило доступа
        rule = self.get_rule(
            user=request.user,
            resource_name=obj.resource.name
        )
        if not rule:
            return False

        if getattr(rule, perm_all, False):
            return True

        if perm_owned and getattr(rule, perm_owned, False):
            return obj.owner == request.user

        return False


class IsAdminUserPermission(BasePermission):
    """Разрешает доступ только пользователям с ролью Admin."""

    def has_permission(self, request, view):
        user = request.user
        # Если нет роли или пользователь не активен — запретить
        if not user.is_authenticated or not user.role:
            return False
        # Разрешаем только админам
        return user.role.name == RoleEnum.ADMIN


class IsSelfOrAdmin(BasePermission):
    """
    Разрешает доступ:
    - администратору ко всем пользователям
    - пользователю/менеджеру только к своему профилю
    """
    def has_object_permission(self, request, view, obj):
        # obj — это пользователь, к которому обращаются
        return request.user.role.name == RoleEnum.ADMIN or obj == request.user
