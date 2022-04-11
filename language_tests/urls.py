from django.urls import path

from language_tests.views import (AdminAddLanguageView, AdminAddQuestionView,
                                  AdminDashboardView, DashboardView, HomeView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('admin-dashboard', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-dashboard/add-language',
         AdminAddLanguageView.as_view(), name='add-language'),
    path('admin-dashboard/add-question',
         AdminAddQuestionView.as_view(), name='add-question')
]
