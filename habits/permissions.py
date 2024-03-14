from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое разрешает только владельцам привычки изменять или удалять ее,
    а также разрешает чтение для всех пользователей, если привычка публичная.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить чтение для всех, если привычка публичная
        if obj.is_public:
            return False

        # Разрешить доступ только владельцу привычки для изменения и удаления
        return obj.owner == request.user


class IsPublicReadOnly(permissions.BasePermission):
    """
    Разрешение, которое разрешает только чтение публичных привычек.
    """

    def has_permission(self, request, view):
        # Разрешить доступ только для чтения, если пользователь аутентифицирован
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить доступ только для чтения, если привычка публичная
        return obj.is_public
