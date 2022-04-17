from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
import logging
from django.http import HttpRequest
from django.contrib.auth.decorators import user_passes_test


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
def calculate_level_view(request):
    if request.COOKIES.get('language_id') is not None:
        langauge_id = request.COOKIES.get('language_id')
        language = Language.objects.get(id=langauge_id)

        questions = language.get_questions()
        results = {'A1': 0, 'A2': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0}
        for i in range(len(questions)):
            selected_answer = request.COOKIES.get(str(i + 1))
            correct_answer = questions[i].answer
            level = questions[i].level

            options = {'Option1': questions[i].option1, 'Option2': questions[i].option2, 'Option3': questions[i].option3,
                       'Option4': questions[i].option4}

            logging.debug(selected_answer)
            logging.debug(options[correct_answer])
            if selected_answer == options[correct_answer]:
                results[str(level)] += 1

        user = User.objects.get(pk=request.user.id)
        result = Result()
        level = max(results, key=results.get)
        result.level = Level.objects.get(level=level)
        result.language = language
        result.user = user
        result.save()

        return HttpResponseRedirect('view-result')
    return HttpResponseRedirect('dashboard')


class ResultView(UserMixin, generic.ListView):
    model = Result
    template_name = 'user/view_result.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).order_by('-date')
