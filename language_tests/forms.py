from django import forms

from . import models


class LanguageForm(forms.ModelForm):
    class Meta:
        model = models.Language
        fields = ['language_name', 'question_number']


class QuestionForm(forms.ModelForm):
    language_id = forms.ModelChoiceField(queryset=models.Language.objects.all(),
                                         empty_label="Назва мови", to_field_name="id")
    level = forms.ModelChoiceField(
        queryset=models.Level.objects.all(), empty_label="Рівень", to_field_name="id")

    class Meta:
        model = models.Question
        fields = ['question', 'option1', 'option2',
                  'option3', 'option4', 'answer']
