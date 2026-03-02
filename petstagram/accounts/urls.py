from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views

app_name = "accounts"

profile_patterns = [
    path('', views.ProfileDetailView.as_view(), name='details'),
    path('edit/', views.ProfileEditView.as_view(), name='edit'),
    path('delete/', views.profile_delete, name='delete'),
]

authentication_patterns = [
    path('register/', views.RegisterAppUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login-page.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', include(authentication_patterns)),
    path('profile/<int:pk>/', include(profile_patterns))
]
