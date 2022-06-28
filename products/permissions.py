from rest_framework import permissions
from users.models import User

class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            return user.is_seller
        return False

class ProductDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
