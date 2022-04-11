from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  View)

from language_tests.forms import LanguageForm, QuestionForm
from language_tests.models import Language, Question


class HomeView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return HttpResponseRedirect('dashboard')
        return render(request, 'index.html')


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
        return render(request, 'admin/dashboard.html')


class AdminAddLanguageView(AdminMixin, CreateView):
    model = Language
    form_class = LanguageForm
    template_name = 'index.html'  # TODO: write html template for form
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        return super().form_valid(form)


class AdminLanguagesView(AdminMixin, ListView):
    model = Language
    template_name = 'index.html'  # TODO: write html template for list


class AdminLanguageView(AdminMixin, DetailView):
    model = Language
    template_name = 'index.html'  # TODO: write html template for language


class AdminDeleteLanguageView(AdminMixin, DeleteView):
    model = Language
    success_url = 'dashboard'


class AdminAddQuestionView(AdminMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'index.html'  # TODO: write html template for add question
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.language_id = self.kwargs['pk']
        return super().form_valid(form)


class AdminQuestionsView(AdminMixin, ListView):
    model = Question
    template_name = 'index.html'  # TODO: write html template


class AdminDeleteQuestionView(AdminMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('dashboard')
