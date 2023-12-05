from rest_framework.permissions import BasePermission
from support.models import Project


class IsContributorAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.auth:
            return False
        if isinstance(obj, Project):
            return obj.contributors.filter(user=request.user).exists()
        return False


class IsAuthorAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.auth:
            return False
        if isinstance(obj, Project):
            return obj.author == request.user
        return False
