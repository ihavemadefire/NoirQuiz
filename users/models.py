from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser to support email as the primary identifier.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where email is the primary key.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # Automatically set when user is created
    last_login = models.DateTimeField(auto_now=True) 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Custom fields
    total_points = models.IntegerField(default=0)  # Overall score
    games_played = models.IntegerField(default=0)  # Total games played
    quizzes_completed = models.IntegerField(default=0)  # Total quizzes completed
    rank = models.CharField(max_length=50, default='Newbie')  # User rank
    badges = models.JSONField(default=list, blank=True)  # List of badges earned

    # Custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # Username is required in addition to email

    def __str__(self):
        return self.email

    # Method to update points
    def add_points(self, points):
        self.total_points += points
        self.save()

    # Method to update rank based on points
    def update_rank(self):
        if self.total_points >= 1000:
            self.rank = 'Legend'
        elif self.total_points >= 500:
            self.rank = 'Pro'
        elif self.total_points >= 100:
            self.rank = 'Intermediate'
        else:
            self.rank = 'Newbie'
        self.save()