from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment
from support.serializers import (
    ProjectSerializer,
    UserSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        author = self.request.GET.get("author")
        type = self.request.GET.get("type")
        if author:
            queryset = queryset.filter(author=author)
        elif type:
            queryset = queryset.filter(type=type)
        return queryset


class IssueViewset(ReadOnlyModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project = self.request.GET.get("project")
        priority = self.request.GET.get("priority")
        if project:
            queryset = queryset.filter(project=project)
        elif priority:
            queryset = queryset.filter(priority=priority)
        return queryset


class CommentViewset(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        project = self.request.GET.get("project")
        issue = self.request.GET.get("issue")
        if project:
            queryset = queryset.filter(project=project)
        elif issue:
            queryset = queryset.filter(issue=issue)
        return queryset


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
