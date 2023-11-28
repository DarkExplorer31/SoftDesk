from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from support.models import Project, Issue, Comment, User

USER = get_user_model()
PASSWORD_RE = r"^[A-Z]{1}[a-z0-9]{6,}[0-9!@#$%^&*()-_+=<>?]{2}$"
USERNAME_TYPE = r"^[A-Za-z0-9]{1,}$"


class ProjectDetailsSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "application_name",
            "description",
            "type",
            "author",
            "author_username",
            "created_time",
            "issues",
            "comments",
        ]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueSerializer(queryset, many=True)
        return serializer.data

    def get_comments(self, instance):
        queryset = instance.issues.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

    def get_author_username(self, instance):
        return instance.author.username


class ProjectListSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "application_name",
            "author",
            "author_username",
            "created_time",
        ]

    def get_author_username(self, instance):
        return instance.author.username


class IssueSerializer(serializers.ModelSerializer):
    project_application_name = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "project",
            "project_application_name",
            "issue_name",
            "status",
            "description",
            "attribution",
            "priority",
            "tag",
            "created_time",
        ]

    def get_project_application_name(self, instance):
        return instance.project.application_name


class CommentSerializer(serializers.ModelSerializer):
    project_application_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "project",
            "project_application_name",
            "description",
            "created_time",
        ]

    def get_project_application_name(self, instance):
        return instance.project.application_name


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=USERNAME_TYPE,
                message="Username must contain only letters and digits."
                + " que des lettres et des chiffres",
            ),
        ],
        error_messages={"blank": "Username cannot be empty."},
    )

    email = serializers.EmailField(
        write_only=True,
        error_messages={"blank": "Email cannot be empty."},
    )
    age = serializers.IntegerField()
    can_be_contacted = serializers.ChoiceField(["Oui", "Non"])
    can_data_be_shared = serializers.ChoiceField(["Oui", "Non"])
    password = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=PASSWORD_RE,
                message="The password must start with an uppercase letter,"
                + " have at least 8 alphanumeric characters and"
                + " end with a digit or a special character.",
            )
        ],
        style={"input_type": "password"},
        error_messages={"blank": "Password cannot be empty."},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        error_messages={"blank": "Password cannot be empty."},
    )

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username already exists.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already exists.")
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return data

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
