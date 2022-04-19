from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail

from language_tests.models import Language, Level, Result
from users.forms import SignUpForm



class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_superuser


class UserDashboardView(UserMixin, generic.ListView):
    template_name = 'user/dashboard.html'
    model = Language


class LanguageView(UserMixin, generic.DetailView):
    template_name = 'user/language.html'
    model = Language


def is_user(user):
    return not user.is_superuser


@user_passes_test(is_user)
def start_test(request, pk):
    language = Language.objects.get(id=pk)
    questions = language.get_questions()

    response = render(request, 'user/start_test.html',
                      {'language': language, 'questions': questions})
    response.set_cookie('language_id', language.id)

    return response


@user_passes_test(is_user)
def calculate_level_view(request: HttpRequest):
    if request.COOKIES.get('language_id') is not None:
        result = save_level_result(request)

        send_mail('Ваш результ з тесту', str(result.level), 'movasite@gmail.com', [request.user.email],
                  fail_silently=False)

        return HttpResponseRedirect('/users/view-result')

    return HttpResponseRedirect('/users/dashboard')


def save_level_result(request):
    langauge_id = request.COOKIES.get('language_id')
    language = Language.objects.get(id=langauge_id)

    results = calculate_level(request, language)

    user = User.objects.get(pk=request.user.id)
    result = Result()

    result.level = Level.objects.get(level=get_level(results))
    result.language = language
    result.user = user
    result.save()

    return result


def calculate_level(request, language):
    questions = language.get_questions()
    results = 0
    for i in range(len(questions)):
        selected_answer = request.COOKIES.get(str(i + 1))
        correct_answer = questions[i].answer

        options = {'Option1': questions[i].option1, 'Option2': questions[i].option2, 'Option3': questions[i].option3,
                   'Option4': questions[i].option4}

        results += selected_answer == options[correct_answer]

    return results


def get_level(scores: int) -> str:
    if 1 <= scores <= 20:
        return 'A1'
    elif 21 <= scores <= 36:
        return 'A2'
    elif 37 <= scores <= 48:
        return 'B1'
    elif 49 <= scores <= 58:
        return 'B2'
    elif 59 <= scores <= 73:
        return 'C1'
    elif 74 <= scores <= 77:
        return 'C2'


class ResultView(UserMixin, generic.ListView):
    model = Result
    template_name = 'user/view_result.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).order_by('-date')
