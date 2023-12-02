from rest_framework.permissions import BasePermission


class IsContributorAuthenticated(BasePermission):
    def has_object_permission(self, request, view):
        pass
