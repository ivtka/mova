from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpRequest
from django.views.generic import View, CreateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from language_tests.forms import LanguageForm, QuestionForm
from language_tests.models import Language, Question


class HomeView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return HttpResponseRedirect('redirection')
        return render(request, '')  # TODO: write html template


class DashboardView(View):
    def get(self, request: HttpRequest):
        if request.user.is_superuser:
            return redirect('admin-dashboard')
        return redirect('user-dashboard')


class AdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AdminDashboardView(AdminMixin, View):
    def get(self, request: HttpRequest):
        return render(request, '')  # TODO: write html template


class AdminAddLanguageView(AdminMixin, CreateView):
    model = models.Language
    form_class = forms.LanguageForm
    template_name = ''  # TODO: write html template for form
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        return super().form_valid(form)


class AdminLanguagesView(AdminMixin, ListView):
    model = models.Language
    template_name = ''  # TODO: write html template for list


class AdminLanguageView(AdminMixin, DetailView):
    model = models.Language
    template_name = ''  # TODO: write html template for language


class AdminDeleteLanguageView(AdminMixin, DeleteView):
    model = models.Language
    success_url = 'dashboard'


class AdminAddQuestionView(AdminMixin, CreateView):
    model = models.Question
    form_class = forms.QuestionForm
    template_name = ''  # TODO: write html template for add question
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.language_id = self.kwargs['pk']
        return super().form_valid(form)


class AdminQuestionsView(AdminMixin, ListView):
    model = models.Question
    template_name = ''  # TODO: write html template


class AdminDeleteQuestionView(AdminMixin, DeleteView):
    model = models.Question
    success_url = reverse_lazy('dashboard')
