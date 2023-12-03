import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Users management
class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        age,
        can_be_contacted=False,
        can_data_be_shared=False,
        password=None,
    ):
        if not email:
            raise ValueError("Email need to be define.")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            age=age,
            can_data_be_shared=can_data_be_shared,
            can_be_contacted=can_be_contacted,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        age,
        can_be_contacted=False,
        can_data_be_shared=False,
        password=None,
    ):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            age=age,
            can_data_be_shared=can_data_be_shared,
            can_be_contacted=can_be_contacted,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    CAN_BE_CONTACTED = [
        ("yes", "Oui"),
        ("no", "Non"),
    ]
    CAN_DATA_BE_SHARED = [
        ("yes", "Oui"),
        ("no", "Non"),
    ]

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField()
    can_be_contacted = models.CharField(
        max_length=10,
        choices=CAN_BE_CONTACTED,
        default="no",
    )
    can_data_be_shared = models.CharField(
        max_length=10,
        choices=CAN_DATA_BE_SHARED,
        default="no",
    )
    created_time = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "age"]

    def __str__(self):
        return self.username


# API objects
class Project(models.Model):
    TYPES = [
        ("back-end", "back-end"),
        ("front-end", "front-end"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="project_author"
    )
    type = models.CharField(
        max_length=100,
        choices=TYPES,
    )
    application_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_contributors(self):
        contributors = Contributor.objects.filter(project=self.application_name)
        contributors_list = list(contributors)
        contributors_list.append(self.author)
        return contributors_list

    def __str__(self):
        return self.application_name


class Contributor(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="contributions"
    )
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Issue(models.Model):
    PRIORITY_ORDER = [("LOW", "Faible"), ("MEDIUM", "Moyen"), ("HIGH", "Haut")]
    TAG_ATTRIBUTION = [
        ("BUG", "bug"),
        ("FEATURE", "Fonctionnalité"),
        ("TASK", "tâche"),
    ]
    STATUS_CHOICES = [
        ("To Do", "A faire"),
        ("In Progress", "En cours"),
        ("Finished", "Terminer"),
    ]
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issues"
    )
    issue_name = models.CharField(max_length=150)
    description = models.TextField(blank=False)
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
    )
    priority = models.CharField(max_length=255, choices=PRIORITY_ORDER)
    attribution = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="issues"
    )
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="issue_author"
    )
    tag = models.CharField(max_length=255, choices=TAG_ATTRIBUTION)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.issue_name


class Comment(models.Model):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="comments"
    )
    issue = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE, related_name="comments"
    )
    description = models.TextField(blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name="comment_author"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
