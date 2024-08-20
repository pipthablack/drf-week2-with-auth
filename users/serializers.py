from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
import logging
from django.urls import reverse
from django.contrib.auth import authenticate
logger = logging.getLogger(__name__)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            logger.warning(f"Attempt to register with existing email: {value}")
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        logger.info(f"User {user.username} registered successfully")
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(request=self.context.get('request'), email=data['email'], password=data['password'])
        if user is None:
            logger.warning(f"Failed login attempt for email: {data['email']}")
            raise serializers.ValidationError('Invalid login credentials')
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {data['email']}")
            raise serializers.ValidationError('User is inactive')
        logger.info(f"User {data['email']} logged in successfully")
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            logger.warning(f"Password reset requested for non-existent email: {value}")
            raise serializers.ValidationError('No user associated with this email.')
        return value

    def save(self):
        request = self.context.get('request')
        user = User.objects.get(email=self.validated_data['email'])
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        subject = 'Password Reset Request'
        message = f'Click the link below to reset your password:\n\n{reset_link}'

        send_mail(subject, message, 'noreply@example.com', [user.email], fail_silently=False)
        logger.info(f"Password reset email sent to {user.email}")

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error(f"Invalid token or user ID during password reset.")
            raise serializers.ValidationError('Invalid token or user ID')

        if not PasswordResetTokenGenerator().check_token(self.user, data['token']):
            logger.warning(f"Invalid or expired token for user ID {uid}")
            raise serializers.ValidationError('Invalid or expired token')

        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        logger.info(f"Password reset successfully for user {self.user.email}")
