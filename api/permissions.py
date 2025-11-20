from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        return obj.user_id == request.user.id
    

class IsAdminOrUserSelf(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated