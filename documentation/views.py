from django.shortcuts import render


def introduction(request):
    return render(request, "documentation/introduction.html")


def about_authentication(request):
    return render(request, "documentation/about_authentication.html")


def about_project(request):
    return render(request, "documentation/about_project.html")


def about_contributor(request):
    return render(request, "documentation/about_contributor.html")


def about_issue(request):
    return render(request, "documentation/about_issue.html")


def about_comment(request):
    return render(request, "documentation/about_comment.html")
