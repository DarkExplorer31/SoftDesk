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
from support.permissions import IsContributorOrAuthor, IsUser


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsContributorOrAuthor, IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributorOrAuthor, IsAuthenticated]

    def get_queryset(self):
        priority = self.request.GET.get("priority")
        queryset = Issue.objects.filter(project__contributors__user=self.request.user)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsContributorOrAuthor, IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(project__contributors__user=self.request.user)
        return queryset


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer


class ContributorViewset(ModelViewSet):
    permission_classes = [IsContributorOrAuthor, IsAuthenticated]
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
