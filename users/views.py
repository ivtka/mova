from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpRequest
from language_tests.models import Language, Question

from users.forms import SignUpForm


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserDashboardView(generic.ListView):
    template_name = 'user/dashboard.html'
    model = Language


class StartTestView(generic.DetailView):
    model = Language
    context_object_name = 'test_context'
    template_name = 'user/start-test.html'

    def get_queryset(self):
        language = Language.objects.get(id=self.kwargs['pk'])
        context = {'language': language,
                   'questions': Question.objects.all().filter(language=language)}
        return context


class TakeTestView(generic.FormView):
    model = Language
    template_name = 'user/take-test.html'

    def get_queryset(self):
        language = Language.objects.get(id=self.kwargs['pk'])
        total_questions = Question.objects.all().filter(language=language).count()
        questions = Question.objects.all().filter(language=language)
        marks = {}
        for question in question:
            if question.level in marks:
                marks[question.level] += 1
            else:
                marks[question.level] = 1

        context = {'language': language, 'marks': marks}


# TODO: Finish View for Calculate level
class CalculateLevelView(generic.View):
    pass


class ResultView(generic.ListView):
    model = Language
    template_name = 'user/result.html'
