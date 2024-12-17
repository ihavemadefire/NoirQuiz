from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'total_points', 'rank', 'games_played', 'quizzes_completed')
    search_fields = ('username', 'email')
    ordering = ('-total_points',)  # Order users by points

admin.site.register(CustomUser, CustomUserAdmin)