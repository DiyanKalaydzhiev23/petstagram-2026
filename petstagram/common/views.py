from django.db.models import Exists, OuterRef
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from common.forms import CommentForm
from common.models import Like
from photos.models import Photo


class HomePageView(ListView):
    context_object_name = "all_photos"
    template_name = "common/home-page.html"
    paginate_by = 1

    def get_queryset(self):
        qs = Photo.objects.prefetch_related('tagged_pets', 'like_set')
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            qs = qs.filter(tagged_pets__name__icontains=pet_name)

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_liked_by_user=Exists(
                    Like.objects.filter(
                        to_photo_id=OuterRef('pk'),
                        user=self.request.user,
                    )
                )
            )
        else:
            qs = qs.annotate(
                is_liked_by_user=Exists(Like.objects.none())
            )

        return qs


def add_comment(request: HttpRequest, photo_pk: int) -> HttpResponse:
    if request.method == "POST":
        photo = Photo.objects.get(pk=photo_pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_pk}')


def like_functionality(request, photo_pk: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_pk, user=request.user).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_pk,
            user=request.user,
        )

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_pk}')


def share_functionality(request, photo_pk: int) -> HttpResponse:
    # This will work only on localhost as it copies the value on the server
    copy(request.META.get('HTTP_REFERER')[:-1] + resolve_url('photos:details', photo_pk))
    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_pk}')
