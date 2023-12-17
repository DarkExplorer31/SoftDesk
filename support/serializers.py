from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation

from support.models import Project, Issue, Comment, User, Contributor

USER = get_user_model()
USERNAME_TYPE = r"^[A-Za-z0-9]{1,}$"
APPLICATION_TYPE = r"^[A-Za-z0-9]{1,}$"


class ContributorSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ["id", "username"]

    def get_id(self, instance):
        return instance.user.id

    def get_username(self, instance):
        return instance.user.username


class ProjectSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    contributors = ContributorSerializer(many=True, read_only=True)

    application_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=APPLICATION_TYPE,
                message="Application name must contain only letters or numbers.",
            ),
        ],
    )

    def validate_application_name(self, value):
        if Project.objects.filter(application_name=value).exists():
            raise serializers.ValidationError("This application name already exists.")
        return value

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        project = super(ProjectSerializer, self).create(validated_data)
        Contributor.objects.create(user=self.context["request"].user, project=project)
        return project

    class Meta:
        model = Project
        fields = [
            "id",
            "application_name",
            "description",
            "type",
            "author_username",
            "created_time",
            "contributors",
            "issues",
            "comments",
        ]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueSerializer(queryset, many=True)
        return serializer.data

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

    def get_author_username(self, instance):
        return instance.author.username


class IssueSerializer(serializers.ModelSerializer):
    def validate_project(self, value):
        if not Project.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("This project not exists.")
        if not Contributor.objects.filter(
            user=self.context["request"].user, project=value
        ).exists():
            raise serializers.ValidationError(
                "You are not a contributor of this project."
            )
        return value

    def validate(self, data):
        project = data.get("project")
        user = data.get("attribution")
        if not Contributor.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError(
                "This user is not a contributor of the project."
            )
        return data

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        issue = super(IssueSerializer, self).create(validated_data)
        return issue

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
    def validate_project(self, value):
        if not Project.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("This project does not exist.")
        if not Contributor.objects.filter(
            user=self.context["request"].user, project=value
        ).exists():
            raise serializers.ValidationError(
                "You are not a contributor of this project."
            )
        return value

    def validate_issue(self, value):
        if not Issue.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("This issue does not exist.")
        project = value.project
        if not Contributor.objects.filter(
            user=self.context["request"].user, project=project
        ).exists():
            raise serializers.ValidationError(
                "You are not a contributor of the project related to this issue."
            )
        return value

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        comment = super(CommentSerializer, self).create(validated_data)
        return comment

    class Meta:
        model = Comment
        fields = [
            "id",
            "project",
            "issue",
            "description",
            "created_time",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=True)
    username = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=USERNAME_TYPE,
                message="Username must contain only letters and digits."
                + " que des lettres et des chiffres",
            ),
        ],
    )
    password = serializers.CharField(
        write_only=True,
        validators=[password_validation.validate_password],
        style={"input_type": "password"},
    )

    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "You need to be at least 15 years old to register."
            )
        if value > 120:
            raise serializers.ValidationError("Invalid age.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password_confirm = validated_data.pop("password_confirm", None)
        user = super(UserRegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
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


class ContributorManagementSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    application_name = serializers.ReadOnlyField(source="project.application_name")
    contributors = ContributorSerializer(many=True, read_only=True)

    def create(self, validated_data):
        contributor = super(ContributorManagementSerializer, self).create(
            validated_data
        )
        return contributor

    def delete(self, instance):
        if instance.project.author == instance.user:
            raise serializers.ValidationError("Cannot delete the author.")
        instance.delete()

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "username",
            "project",
            "contributors",
            "application_name",
            "created_time",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
