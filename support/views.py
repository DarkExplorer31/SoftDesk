from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment, Contributor, User
from support.serializers import (
    ProjectSerializer,
    UserRegistrationSerializer,
    IssueSerializer,
    CommentSerializer,
    CreateContributorSerializer,
)
from support.permissions import IsContributorAuthenticated, IsAuthorAuthenticated


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsContributorAuthenticated, IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.filter(contributors__user=self.request.user)
        application_name = self.request.GET.get("application_name")
        if application_name:
            queryset = queryset.filter(application_name=application_name)
        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributorAuthenticated, IsAuthenticated]

    def get_queryset(self):
        queryset = Issue.objects.all()
        project = self.request.GET.get("project")
        priority = self.request.GET.get("priority")
        if project:
            queryset = queryset.filter(project=project)
        elif priority:
            queryset = queryset.filter(priority=priority)
        return queryset


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsContributorAuthenticated, IsAuthenticated]

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
    serializer_class = UserRegistrationSerializer


class ContributorManageView(CreateAPIView):
    model = Contributor
    queryset = User.objects.all()
    permission_classes = [IsAuthorAuthenticated, IsAuthenticated]
    serializer_class = CreateContributorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["application_name"] = self.kwargs["application_name"]
        return context
