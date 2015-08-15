from rest_framework import permissions


class EventPermission(permissions.BasePermission):
    """
    create for authenticated user only
    update/destroy for event admin only
    readonly for everyone else
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.admin == request.user


class IsObjectUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAnonUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            return False
        else:
            return True
