from rest_framework import permissions


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, req, view) -> bool:
        if req.method in permissions.SAFE_METHODS:
            return True

        if req.user.is_authenticated and req.user.is_superuser:
            return True

        return False
