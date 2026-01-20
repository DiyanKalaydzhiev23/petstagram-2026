from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def register(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/register-page.html')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/login-page.html')


def profile_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile-details-page.html')


def profile_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile-edit-page.html')


def profile_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'accounts/profile-delete-page.html')
