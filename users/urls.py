from django.urls import path
from .views import CustomTokenObtainPairView, LogoutView, SignupView, UserListView, UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout
    path('signup/', SignupView.as_view(), name='signup'),  # Signup
    path('', UserListView.as_view(), name='user_list'),  # User list
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),  # User detail
]
