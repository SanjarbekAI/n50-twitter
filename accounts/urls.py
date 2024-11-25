from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('verify/resend/', views.ResendVerificationEmailView.as_view(), name='verify-resend'),
    path('me/', views.ProfileView.as_view(), name='profile'),

    # following
    path('following/', views.FollowingAPIView.as_view(), name='following')

]
