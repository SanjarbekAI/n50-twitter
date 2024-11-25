from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import UserModel, VerificationModel, FollowerModel


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, max_length=50)

    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return UserModel.objects.create_user(**validated_data)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Passwords do not match')

        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return attrs

    def validate_email(self, email):
        if not email.endswith('@gmail.com') or email.count('@') != 1:
            raise serializers.ValidationError('Gmail is not correct')
        return email


class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        try:
            user = UserModel.objects.get(email=attrs['email'])
            user_code = VerificationModel.objects.get(user=user, code=attrs['code'])
        except VerificationModel.DoesNotExist:
            raise serializers.ValidationError('Gmail or code is not valid')

        current_time = timezone.now()
        if user_code.created_at + timedelta(minutes=2) < current_time:
            user_code.delete()
            raise serializers.ValidationError("This code is already expired")

        attrs['user_code'] = user_code
        return attrs


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=50)
    error_message = "Email/Username or password is not valid"

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')
        try:
            if email_or_username.endswith('@gmail.com'):
                user = UserModel.objects.get(email=email_or_username)
            else:
                user = UserModel.objects.get(username=email_or_username)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(self.error_message)

        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise serializers.ValidationError(self.error_message)

        attrs['user'] = authenticated_user
        return attrs


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = UserModel.objects.get(email=email, is_active=False)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('Email does not exist')

        user_code = VerificationModel.objects.filter(user__email=email)
        if user_code:
            current_time = timezone.now()
            if user_code.created_at + timedelta(minutes=2) > current_time:
                raise serializers.ValidationError("You already have active code")

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser']
        read_only_fields = ['is_active', 'date_joined', 'last_login', 'is_staff']


class FollowingSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())

    class Meta:
        model = FollowerModel
        fields = ['created_at', 'to_user']

    def is_follow_back(self, obj):
        follow_type = self.context.get('request').query_params.get('type')
        if follow_type == 'followers':
            return FollowerModel.objects.filter(user=obj.user, to_user=obj.to_user).exists()
        return FollowerModel.objects.filter(user=obj.to_user, to_user=obj.user).exists()

    def to_representation(self, instance):
        data = dict()
        data['first_name'] = instance.to_user.first_name
        data['last_name'] = instance.to_user.last_name
        data['username'] = instance.to_user.username
        data['follow_back'] = self.is_follow_back(instance)
        return data
