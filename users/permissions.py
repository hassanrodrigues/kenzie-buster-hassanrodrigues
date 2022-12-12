from rest_framework import permissions


class PermissionsPersonalized(permissions.BasePermission):
    def has_object_permission(self, req, view, obj) -> bool:
        if req.user.is_superuser:
            return True

        return req.user == obj
