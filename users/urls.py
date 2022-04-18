from django.urls import path

from users.views import (LanguageView, ResultView, UserDashboardView, UserRegisterView,
                         start_test, calculate_level_view)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate_view, name='activate'),
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('dashboard/language/<int:pk>/', LanguageView.as_view(), name='language'),
    path('dashboard/language/start-test/<int:pk>/',
         start_test, name='start_test'),
    path('calculate-level/', calculate_level_view, name="calculate-view"),
    path('view-result/', ResultView.as_view(), name='view-result')
]
