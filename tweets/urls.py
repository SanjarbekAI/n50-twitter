from django.urls import path
from rest_framework.routers import DefaultRouter

from tweets import views

app_name = "tweets"

router = DefaultRouter()
router.register(r'', views.TweetViewSet)

urlpatterns = [
    path('child/', views.TweetChildListAPIView.as_view())
] + router.urls
