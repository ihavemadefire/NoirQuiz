from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db import IntegrityError
from .serializers import CustomUserSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    A custom implementation of TokenObtainPairView if additional data
    or behavior needs to be added.
    """
    pass


class LogoutView(APIView):
    """
    Handles user logout by blacklisting the provided refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"detail": "Logout successful."}, status=200)
        except AttributeError:
            return Response({"error": "Token blacklisting is not enabled."}, status=501)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class SignupView(APIView):
    """
    Handles user signup by creating a new user with validated data.
    """
   
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Basic validation
        if not username or not email or not password or not confirm_password:
            return Response({"error": "All fields are required."}, status=400)
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=400)

        # Validate password strength
        try:
            validate_password(password)
        except DjangoValidationError as e:
            return Response({"error": e.messages}, status=400)        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({"detail": "User created successfully."}, status=201)
        except IntegrityError as e:
            if "unique constraint" in str(e).lower():
                if "email" in str(e).lower():
                    return Response({"error": {"email": "A user with this email already exists."}}, status=400)
                if "username" in str(e).lower():
                    return Response({"error": {"username": "A user with this username already exists."}}, status=400)
            if "NOT NULL constraint failed" in str(e).lower():
                return Response({"error": "A required field is missing or not properly set."}, status=400)
            return Response({"error": "An error occurred during signup."}, status=400)
        
class UserListView(APIView):
    """
    
    View to retrieve all users.
    """
    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    View to retrieve a single user by their email.
    """
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)