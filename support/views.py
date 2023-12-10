from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import MethodNotAllowed
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
        application_name = self.request.GET.get("application_name")
        if application_name:
            queryset = queryset.filter(application_name=application_name)
        return queryset


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributor, IsAuthenticated]

    def get_queryset(self):
        queryset = Issue.objects.all()
        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.author.id:
            return super().destroy(request, *args, **kwargs)
        else:
            raise MethodNotAllowed("DELETE")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.author.id:
            return super().update(request, *args, **kwargs)
        else:
            raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.author.id:
            return super().partial_update(request, *args, **kwargs)
        else:
            raise MethodNotAllowed("PATCH")


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsContributor, IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue = self.request.GET.get("issue")
        if issue:
            queryset = queryset.filter(issue=issue)
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
