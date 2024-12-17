from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'total_points', 'games_played', 'quizzes_completed',
            'rank', 'badges', 'date_joined', 'last_login'
        ]
