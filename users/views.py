from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from django.contrib.auth import get_user_model,authenticate
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import UserSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    This view is responsible for handling user registration.
    It uses a CreateAPIView from Django REST Framework, which automatically handles POST requests.

    Attributes:
    queryset: The queryset of all User objects.
    serializer_class: The serializer class used for validating and serializing user data.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(views.APIView):
    """
    This view is responsible for handling user login.
    It uses a generic APIView from Django REST Framework, which allows for custom handling of POST requests.

    Methods:
    post: Handles the POST request for user login.

    Attributes:
    permission_classes: The permission classes required for accessing this view. In this case, no permissions are required.
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        tokens = self.generate_tokens(user)
        return Response({'email': user.email, 'tokens': tokens}, status=status.HTTP_200_OK)

    def generate_tokens(self, user):
        """
        Generates refresh and access tokens for the given user.

        Parameters:
        user (User): The user for whom tokens are to be generated.

        Returns:
        dict: A dictionary containing the refresh and access tokens.

        Raises:
        APIException: If token generation fails.
        """
        try:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        except Exception as e:
            raise APIException(detail='Token generation failed')


class PasswordResetView(generics.GenericAPIView):
    """
    This view is responsible for handling password reset requests.
    It uses a generic APIView from Django REST Framework, which allows for custom handling of POST requests.

    Methods:
    post: Handles the POST request for password reset.

    Attributes:
    serializer_class: The serializer class used for validating and serializing password reset data.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset link sent."})


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    This view is responsible for handling password reset confirmation.
    It uses a generic APIView from Django REST Framework, which allows for custom handling of POST requests.

    Methods:
    post: Handles the POST request for password reset confirmation.

    Attributes:
    serializer_class: The serializer class used for validating and serializing password reset confirmation data.
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."})


class LogoutView(views.APIView):
    """
    This view is responsible for handling user logout.
    It uses a generic APIView from Django REST Framework, which allows for custom handling of POST requests.

    Methods:
    post: Handles the POST request for user logout.

    Attributes:
    permission_classes: The permission classes required for accessing this view. In this case, only authenticated users can access it.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    This view is responsible for listing all users (Admin only).
    It uses a ListAPIView from Django REST Framework, which automatically handles GET requests.

    Attributes:
    queryset: The queryset of all User objects.
    serializer_class: The serializer class used for serializing user data.
    permission_classes: The permission classes required for accessing this view. In this case, only admin users can access it.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only accessible by admin users


class UserDetailView(generics.RetrieveAPIView):
    """
    This view is responsible for retrieving a user by ID (Admin only).
    It uses a RetrieveAPIView from Django REST Framework, which automatically handles GET requests.

    Attributes:
    queryset: The queryset of all User objects.
    serializer_class: The serializer class used for serializing user data.
    permission_classes: The permission classes required for accessing this view. In this case, only admin users can access it.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only accessible by admin users


class UserDeleteView(generics.DestroyAPIView):
    """
    This view is responsible for deleting a user (Admin only).
    It uses a DestroyAPIView from Django REST Framework, which automatically handles DELETE requests.

    Attributes:
    queryset: The queryset of all User objects.
    serializer_class: The serializer class used for serializing user data.
    permission_classes: The permission classes required for accessing this view. In this case, only admin users can access it.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only accessible by admin users