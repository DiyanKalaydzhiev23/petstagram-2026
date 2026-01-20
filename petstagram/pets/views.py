from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def pet_add(request: HttpRequest) -> HttpResponse:
    return render(request, 'pets/pet-add-page.html')


def pet_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-details-page.html')


def pet_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-edit-page.html')


def pet_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-delete-page.html')
