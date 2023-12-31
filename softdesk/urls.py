"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from documentation.views import (
    introduction,
    about_authentication,
    about_project,
    about_contributor,
    about_issue,
    about_comment,
)

from support.views import (
    ProjectViewset,
    RegisterView,
    IssueViewset,
    CommentViewset,
    ContributorViewset,
    UserViewset,
)


router = routers.SimpleRouter()
router.register("project", ProjectViewset, basename="Project")
router.register("issue", IssueViewset, basename="Issue")
router.register("comment", CommentViewset, basename="Comment")
router.register("contributor", ContributorViewset, basename="Contributor")
router.register("user", UserViewset, basename="User")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api/", include(router.urls)),
    # user endpoint
    path("api/register/", RegisterView.as_view()),
    # documentation
    path("", introduction, name="introduction"),
    path("authentication-doc/", about_authentication, name="authentication_doc"),
    path("project-doc/", about_project, name="project_doc"),
    path("contributor-doc/", about_contributor, name="contributor_doc"),
    path("issue-doc/", about_issue, name="issue_doc"),
    path("comment-doc/", about_comment, name="comment_doc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
