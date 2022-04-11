from django.urls import path

from language_tests.views import HomeView, DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard', DashboardView.as_view(), name='dashboard')
]