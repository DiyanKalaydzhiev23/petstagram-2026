from django.urls import path, include
from pets import views

app_name = 'pets'

urlpatterns = [
    path('add/', views.pet_add, name='add'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', views.pet_details, name='details'),
        path('edit/', views.pet_edit, name='edit'),
        path('delete/', views.pet_delete, name='delete'),
    ]))
]
