from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment
from support.serializers import (
    ProjectsSerializer,
    UsersSerializer,
    IssuesSerializer,
    CommentsSerializer,
)


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        author = self.request.GET.get("author")
        type = self.request.GET.get("type")
        if author:
            queryset = queryset.filter(author=author)
        elif type:
            queryset = queryset.filter(type=type)
        return queryset
