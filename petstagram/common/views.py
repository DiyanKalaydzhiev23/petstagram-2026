from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from common.forms import CommentForm, SearchForm
from common.models import Like, Comment
from photos.models import Photo


class HomePageView(ListView):
    queryset = Photo.objects.prefetch_related('tagged_pets', 'like_set')
    context_object_name = "all_photos"
    template_name = "common/home-page.html"
    paginate_by = 1

    def get_queryset(self):
        qs = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            qs = qs.filter(tagged_pets__name__icontains=pet_name)

        return qs

#
# def home_page(request: HttpRequest) -> HttpResponse:
#     form = SearchForm(request.GET or None)
#     all_photos = Photo.objects.prefetch_related('tagged_pets', 'like_set')
#
#     if request.GET and form.is_valid():
#         searched_name = form.cleaned_data['pet_name']
#         all_photos = all_photos.filter(tagged_pets__name__icontains=searched_name)
#
#     context = {
#         'all_photos': all_photos,
#     }
#
#     return render(request, 'common/home-page.html', context)


def add_comment(request: HttpRequest, photo_pk: int) -> HttpResponse:
    if request.method == "POST":
        photo = Photo.objects.get(pk=photo_pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_pk}')


def like_functionality(request, photo_pk: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_pk).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_pk,
        )

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_pk}')


def share_functionality(request, photo_pk: int) -> HttpResponse:
    # This will work only on localhost as it copies the value on the server
    copy(request.META.get('HTTP_REFERER')[:-1] + resolve_url('photos:details', photo_pk))
    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_pk}')
