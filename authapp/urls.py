from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, UserDetailView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
]