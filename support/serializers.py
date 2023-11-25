from rest_framework import serializers
from django.contrib.auth import get_user_model

from support.models import Project, Issue, Comment

USER = get_user_model()


class ProjectsSerializer(serializers.ModelSerializer):
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
