from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from photos.forms import PhotoForm
from photos.models import Photo


def photo_add(request: HttpRequest) -> HttpResponse:
    form = PhotoForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('common:home')

    context = {
        'form': form,
    }

    return render(request, 'photos/photo-add-page.html', context)


def photo_details(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.prefetch_related('tagged_pets', 'like_set', 'comment_set').get(pk=pk)

    context = {
        'photo': photo,
    }

    return render(request, 'photos/photo-details-page.html', context)


def photo_edit(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.get(pk=pk)
    form = PhotoForm(request.POST or None, request.FILES or None, instance=photo)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('photos:details', photo.pk)

    context = {
        'form': form,
    }

    return render(request, 'photos/photo-edit-page.html', context)


def photo_delete(request: HttpRequest, pk: int) -> HttpResponse:
    Photo.objects.get(pk=pk).delete()
    return redirect('common:home')

