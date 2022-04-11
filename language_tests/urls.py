from django.urls import path

from language_tests.views import HomeView, DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('redirection', DashboardView.as_view(), name='redirection')
]