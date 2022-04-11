from django.urls import path
from users.views import UserDashboardView, UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('dashboard', UserDashboardView.as_view(), name='user-dashboard'),
]
