from lib2to3.fixes.fix_input import context

from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from pets.forms import PetForm
from pets.models import Pet
from photos.models import Photo


def pet_add(request: HttpRequest) -> HttpResponse:
    form = PetForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('accounts:details', pk=1)

    context = {
        "form": form,
    }

    return render(request, 'pets/pet-add-page.html', context)


def pet_details(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
    pet = Pet.objects.prefetch_related(
        Prefetch(
            'photo_set',
            queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
        )
    ).get(slug=pet_slug)

    context = {
        "pet": pet,
    }

    return render(request, 'pets/pet-details-page.html', context)


def pet_edit(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
    pet = Pet.objects.get(slug=pet_slug)
    form = PetForm(request.POST or None, instance=pet)

    if request.method == "POST" and form.is_valid():
        instance = form.save()
        return redirect('pets:details', username='username', pet_slug=instance.slug)

    context = {
        'pet': pet,
        'form': form,
    }

    return render(request, 'pets/pet-edit-page.html', context)


def pet_delete(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
    pet = Pet.objects.get(slug=pet_slug)
    form = PetForm(request.POST or None, instance=pet)

    if request.method == "POST" and form.is_valid():
        pet.delete()
        return redirect('accounts:details', pk=1)

    context = {
        'pet': pet,
        'form': form,
    }

    return render(request, 'pets/pet-delete-page.html', context)
