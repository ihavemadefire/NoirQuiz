from django.contrib import admin
from django.urls import path, include
from core.views import HomePageView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , HomePageView.as_view() , name = 'home'),
    path('api/v1/movies', include('movies.urls')),
    path('api/v1/users/', include('users.urls')),  # Adjust path as needed

]
