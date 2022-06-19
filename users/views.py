from statistics import mode
from typing import Tuple

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
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
        result, precentage = save_level_result(request)

        response = render(request, 'user/result.html',
                          {'result': result, 'precentage': precentage})
        return response

    return HttpResponseRedirect('/users/dashboard')


def save_level_result(request):
    language_id = request.COOKIES.get('language_id')
    language = Language.objects.get(id=language_id)

    results = calculate_level(request, language)

    user = User.objects.get(pk=request.user.id)
    result = Result()

    level, precentage = get_level(results)

    result.level = Level.objects.get(level=level)
    result.language = language
    result.user = user
    result.save()

    return (result, precentage)


def calculate_level(request, language):
    questions = language.get_questions()
    results = 0
    for i in range(len(questions)):
        selected_answer = request.POST.get(str(i + 1))
        correct_answer = questions[i].answer

        options = {'Option1': questions[i].option1,
                   'Option2': questions[i].option2,
                   'Option3': questions[i].option3,
                   'Option4': questions[i].option4}

        results += selected_answer == options[correct_answer]

    return results


def get_level(scores: int) -> Tuple[str, int]:
    level = 'A1'
    precentage = 100
    print(scores)

    if scores >= 1 and scores <= 20:
        level = 'A1'
        precentage = scores / 20 * 100
    elif scores >= 21 and scores <= 36:
        level = 'A2'
        precentage = (scores - 20) / 16 * 100
    elif scores >= 37 and scores <= 48:
        level = 'B1'
        precentage = (scores - 36) / 12 * 100
    elif scores >= 49 and scores <= 58:
        level = 'B2'
        precentage = (scores - 48) / 10 * 100
    elif scores >= 59 and scores <= 73:
        level = 'C1'
        precentage = (scores - 58) / 8 * 100
    elif scores >= 74 and scores <= 77:
        level = 'C2'
        precentage = (scores - 73) / 5 * 100

    return (level, 100 - precentage)


class ResultsView(UserMixin, generic.ListView):
    model = Result
    template_name = 'user/view_result.html'
    context_object_name = 'results'

    def get_queryset(self):
        results = Result.objects.filter(
            user=self.request.user).order_by('-date')
        return {'results': results, 'average': self.frequence()}

    def frequence(self):
        tmp = [row['level'] for row in Result.objects.values('level')]
        level = mode(tmp)
        levels = {1: 'A1', 2: 'A2', 3: 'B1', 4: 'B2', 5: 'C1', 6: 'C2'}
        return levels[level]
