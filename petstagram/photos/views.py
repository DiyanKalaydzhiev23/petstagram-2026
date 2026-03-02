from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView

from common.mixin import CheckUserIsOwner
from common.models import Like
from photos.forms import PhotoForm
from photos.models import Photo


def photo_add(request: HttpRequest) -> HttpResponse:
    form = PhotoForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        return redirect('common:home')

    context = {
        'form': form,
    }

    return render(request, 'photos/photo-add-page.html', context)


def photo_details(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.prefetch_related('tagged_pets', 'like_set', 'comment_set')

    if request.user.is_authenticated:
        photo = photo.annotate(
            is_liked_by_user=Exists(
                Like.objects.filter(
                    to_photo_id=OuterRef('pk'),
                    user=request.user,
                )
            )
        )
    else:
        photo = photo.annotate(
            is_liked_by_user=Exists(Like.objects.none())
        )

    photo = photo.get(pk=pk)

    context = {
        'photo': photo,
    }

    return render(request, 'photos/photo-details-page.html', context)


class PhotoEditView(LoginRequiredMixin, CheckUserIsOwner, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self) -> str:
        return reverse(
            'photos:details',
            kwargs={"pk": self.object.pk},
        )


class PhotoDeleteView(LoginRequiredMixin, CheckUserIsOwner, DeleteView):
    model = Photo
    success_url = reverse_lazy('common:home')

