from rest_framework import serializers
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment

USER = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "application_name",
            "description",
            "type",
            "author",
            "created_time",
        ]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "project",
            "issue_name",
            "status",
            "description",
            "attribution",
            "priority",
            "tag",
            "created_time",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "project", "issue", "description", "created_time"]
