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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    age = serializers.IntegerField()
    can_be_contacted = serializers.ChoiceField(["Oui", "Non"])
    can_data_be_shared = serializers.ChoiceField(["Oui", "Non"])
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def create(self, validated_data):
        user = USER.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            age=validated_data["age"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = USER
        fields = [
            "id",
            "username",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "password",
            "password_confirm",
        ]
