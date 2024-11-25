import threading

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import UserModel, FollowerModel
from accounts.serializers import RegisterSerializer, VerificationSerializer, LoginSerializer, ResendCodeSerializer, \
    UserSerializer, FollowingSerializer
from accounts.signals import send_verification_email


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        return user


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_code = serializer.validated_data['user_code']
        user = user_code.user

        user.is_active = True
        user.save()
        user_code.delete()
        response = {
            "success": True,
            "message": "Email verified successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user=user)
        response = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        user.last_login = timezone.now()
        user.save()
        return Response(response, status=status.HTTP_200_OK)


class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        email_thread = threading.Thread(target=send_verification_email, args=(email,))
        email_thread.start()
        response = {
            "success": True,
            "message": "New code sent to email"
        }
        return Response(response, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def get_object(self):
        return self.request.user


class FollowingAPIView(APIView):
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FollowingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        to_user = serializer.validated_data['to_user']
        response = {"success": True}

        following = FollowerModel.objects.filter(user=user, to_user=to_user)
        if following.exists():
            following.delete()
            response['detail'] = "You have been unfollowed successfully"
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        FollowerModel.objects.create(user=user, to_user=to_user)

        response['detail'] = "You have been followed successfully"
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request):
        follow_type = self.request.query_params.get('type')
        qs = self.request.user.following.all()
        if follow_type == "followers":
            qs = self.request.user.followers.all()
        serializer = FollowingSerializer(qs, many=True, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
