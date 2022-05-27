from django.urls import path

from users.views import (ResultsView, UserDashboardView, UserRegisterView,
                         start_test, calculate_level_view)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('dashboard/language/start-test/<int:pk>/',
         start_test, name='start_test'),
    path('calculate-level/', calculate_level_view, name="calculate-view"),
    path('dashboard/view-result/', ResultsView.as_view(), name='view-result')
]
