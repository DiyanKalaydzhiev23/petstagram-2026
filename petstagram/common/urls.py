from django.urls import path
from common import views

app_name = 'common'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('<int:photo_pk>/like/', views.like_functionality, name='like'),
    path('<int:photo_pk>/share/', views.share_functionality, name='share'),
    path('<int:photo_pk>/comment/', views.add_comment, name='add-comment'),
]
