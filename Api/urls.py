from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('', include(router.urls)),  # Your main url path
    path('home/', views.homepage),  # Your endpoint here
    path('watchlist/', views.WatchListAPIView.as_view()),  # Your endpoint here
    path('watchlist/<int:pk>/', views.WatchListDetailView.as_view()),  # Your endpoint here
    # path('stream_platforms/', views.StreamPlatform.as_view()),  # Your endpoint here
    # path('stream_platforms/<int:pk>', views.StreamPlatformDetailView.as_view()),  # Your endpoint here
    path('stream/<int:pk>/review/', views.ReviewList.as_view()),  # Your endpoint here
    path('<int:pk>/review-create/', views.ReviewCreate.as_view()),  # Your endpoint here
    path('stream/review/<int:pk>/', views.ReviewDetails.as_view()),  # Your endpoint here

]