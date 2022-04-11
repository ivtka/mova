from django.urls import path

from users.views import StartTestView, TakeTestView, UserDashboardView, UserRegisterView, LanguageView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('dashboard/language/<int:pk>', LanguageView.as_view(), name='language'),
    path('dashboard/language/<int:pk>/start-test',
         StartTestView.as_view(), name='start-test'),
    path('dashboard/language/<int:pk>/take-test',
         TakeTestView.as_view(), name='take-test')
]
