from django import forms

from language_tests.models import Language, Question, Level


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language_name', 'question_number']


class QuestionForm(forms.ModelForm):
    language_id = forms.ModelChoiceField(queryset=Language.objects.all(),
                                         empty_label="Назва мови", to_field_name="id")
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(), empty_label="Рівень", to_field_name="id")

    class Meta:
        model = Question
        fields = ['question', 'option1', 'option2',
                  'option3', 'option4', 'answer']
