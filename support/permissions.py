from rest_framework.permissions import BasePermission, SAFE_METHODS
from support.models import Project


class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.contributors.filter(user=request.user).exists()
        return False


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.author == request.user
        return False


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "GET":
            return True
        elif request.method == "PUT":
            return obj.user == request.user
        elif request.method == "PATCH":
            return obj.user == request.user
        elif request.method == "DELETE":
            return obj.user == request.user
        return False
