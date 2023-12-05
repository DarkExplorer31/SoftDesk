from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from support.models import Project, Issue, Comment, User, Contributor

USER = get_user_model()
PASSWORD_RE = r"^[A-Za-z0-9]{6,}[0-9!@#$%^&*()-_+=<>?]{,2}$"
USERNAME_TYPE = r"^[A-Za-z0-9]{1,}$"
APPLICATION_TYPE = r"^[A-Za-z]{1,}$"


class ContributorSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ["username"]

    def get_username(self, instance):
        return instance.user.username


class ProjectSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    contributors = ContributorSerializer(many=True, read_only=True)

    type = serializers.ChoiceField(
        [
            ("back-end", "back-end"),
            ("front-end", "front-end"),
            ("iOS", "iOS"),
            ("Android", "Android"),
        ],
        error_messages={"blank": "Type cannot be empty."},
    )
    application_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=APPLICATION_TYPE,
                message="Application name must contain only letters.",
            ),
        ],
        error_messages={"blank": "Application name cannot be empty."},
    )
    description = serializers.CharField(
        error_messages={"blank": "Description cannot be empty."}
    )

    def validate(self, data):
        application_name = data.get("application_name")
        description = data.get("description")
        if Project.objects.filter(application_name=application_name).exists():
            raise serializers.ValidationError("This application name already exists.")

        if Project.objects.filter(description=description).exists():
            raise serializers.ValidationError("This description already exists.")
        return data

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        project = Project.objects.create(
            application_name=validated_data["application_name"],
            description=validated_data["description"],
            type=validated_data["type"],
            author=validated_data["author"],
        )
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
        queryset = instance.issues.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

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


class UserRegistrationSerializer(serializers.ModelSerializer):
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
                message="The password must have least 8"
                + " alphanumeric characters and"
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


class ContributorManagementSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    application_name = serializers.ReadOnlyField(source="project.application_name")

    def validate(self, data):
        user = data["user"]
        project = data["project"]
        existing_contributor = Contributor.objects.filter(user=user, project=project)
        if existing_contributor:
            raise serializers.ValidationError(
                "Contributor already exists for this user and project."
            )
        return data

    def create(self, validated_data):
        contributor = Contributor.objects.create(
            user=validated_data["user"], project=validated_data["project"]
        )
        return contributor

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "username",
            "project",
            "application_name",
            "created_time",
        ]
