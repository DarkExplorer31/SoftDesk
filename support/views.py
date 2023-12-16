from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment, Contributor, User
from support.serializers import (
    ProjectSerializer,
    UserRegistrationSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorManagementSerializer,
    UserSerializer,
)
from support.permissions import IsContributor, IsAuthor, IsUser


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsContributor, IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributor, IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        priority = self.request.GET.get("priority")
        queryset = []
        issue_id = self.kwargs.get("pk")
        issues = Issue.objects.all()
        if issue_id:
            return issues.filter(id=issue_id)
        if project_id:
            queryset = issues.filter(project=project_id)
        if priority:
            queryset = issues.filter(priority=priority)
        return queryset


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsContributor, IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        issue_id = self.request.GET.get("issue_id")
        queryset = []
        comment_id = self.kwargs.get("pk")
        comments = Comment.objects.all()
        if comment_id:
            return comments.filter(id=comment_id)
        if project_id and issue_id:
            queryset = comments.filter(project=project_id, issue=issue_id)
        return queryset


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer


class ContributorViewset(ModelViewSet):
    permission_classes = [IsAuthor, IsAuthenticated]
    serializer_class = ContributorManagementSerializer
    queryset = Contributor.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Contributor.objects.filter(user=user)
        return queryset


class UserViewset(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUser]
