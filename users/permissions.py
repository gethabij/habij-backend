# users/permissions.py
from rest_framework import permissions


class IsUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.id == request.user.id
