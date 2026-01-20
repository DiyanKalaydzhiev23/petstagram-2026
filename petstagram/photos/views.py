from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def photo_add(request: HttpRequest) -> HttpResponse:
    return render(request, 'photos/photo-add-page.html')


def photo_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'photos/photo-details-page.html')


def photo_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'photos/photo-edit-page.html')
