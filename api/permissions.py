from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user.is_staff:
            return True

        return obj.author == request.user
#
#
# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.user.is_authenticated:
#             return request.user == request.user.is_superuser or request.user.is_staff


# class IsOwnerOrAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in ('GET','HEAD','OPTIONS'):
#             return True
#         elif request.user.is_staff:
#             return True
#
#         elif obj.author == request.user:
#             return True
#         else:
#             return False


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        admin_permission = super().has_permission(request, view)
        return request.method == 'GET' or admin_permission


# class IsOwnerOrAdmin(permissions.IsAdminUser):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if obj.author == request.user:
#             return True
#         return super().has_object_permission(request, view, obj)
