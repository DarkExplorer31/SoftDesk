from rest_framework.permissions import BasePermission, SAFE_METHODS
from support.models import Project


class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            try:
                return obj.contributors.filter(user=request.user).exists()
            except AttributeError:
                return obj.project.contributors.filter(user=request.user).exists()
        return False


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["POST", "DELETE"]:
            project_id = request.data.get("project", None)
            if project_id:
                try:
                    project = Project.objects.get(id=project_id)
                    return project.author == request.user
                except Project.DoesNotExist:
                    return False
        return False


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            return obj == request.user
        return False
