from rest_framework import permissions
from users.models import User

class UpdateUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
        
class UpdateUserActivePermission(permissions.BasePermission):
    message = "You can't update is_active property"

    def has_permission(self, request, view):
        if 'is_active' in request.data:
            return False
        return True

class DeactivatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser