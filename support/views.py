from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment
from support.serializers import (
    ProjectDetailsSerializer,
    ProjectListSerializer,
    UserSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewset(ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailsSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        application_name = self.request.GET.get("application_name")
        author = self.request.GET.get("author")
        if application_name:
            queryset = queryset.filter(application_name=application_name)
        elif author:
            queryset = queryset.filter(author=author)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


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
