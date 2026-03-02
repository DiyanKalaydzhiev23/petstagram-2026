from django.db.models import Exists, OuterRef, Prefetch
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from common.mixin import CheckUserIsOwner
from common.models import Like
from pets.forms import PetForm
from pets.models import Pet
from photos.models import Photo


class PetAddView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html'

    def get_success_url(self):
        return reverse('accounts:details', kwargs={"pk": self.object.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PetDetailView(DetailView):
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-details-page.html"

    def get_queryset(self):
        photo_queryset = Photo.objects.prefetch_related('tagged_pets', 'like_set')

        if self.request.user.is_authenticated:
            photo_queryset = photo_queryset.annotate(
                is_liked_by_user=Exists(
                    Like.objects.filter(
                        to_photo_id=OuterRef('pk'),
                        user=self.request.user,
                    )
                )
            )
        else:
            photo_queryset = photo_queryset.annotate(
                is_liked_by_user=Exists(Like.objects.none())
            )

        return Pet.objects.prefetch_related(
            Prefetch('photo_set', queryset=photo_queryset)
        )


class PetEditView(CheckUserIsOwner, UpdateView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-edit-page.html"

    def test_func(self) -> bool:
        return self.request.user == self.get_object().user

    def get_success_url(self) -> str:
        return reverse(
            'pets:details',
            kwargs={
                "username": 'username', "pet_slug": self.object.slug
            }
        )


class PetDeleteView(DeleteView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-delete-page.html"

    def get_success_url(self):
        return reverse('accounts:details', kwargs={"pk": self.object.user.pk})

    def get_initial(self):
        return self.object.__dict__
