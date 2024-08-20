# urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/',  views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]
