from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsContributorOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            try:
                return obj.contributors.filter(user=request.user).exists()
            except AttributeError:
                return obj.project.contributors.filter(user=request.user).exists()
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.author == request.user
        return False


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            return obj == request.user
        return False
