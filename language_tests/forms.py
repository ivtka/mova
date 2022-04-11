from django import forms

from language_tests.models import Language, Level, Question


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language_name', 'max_questions']


class QuestionForm(forms.ModelForm):
    language_id = forms.ModelChoiceField(queryset=Language.objects.all(),
                                         empty_label="Назва мови", to_field_name="id")
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(), empty_label="Рівень", to_field_name="id", widget=forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-1/4 p-2.5'}))

    class Meta:
        model = Question
        fields = ['question', 'level', 'option1', 'option2',
                  'option3', 'option4', 'answer']
        widgets = {
            'answer': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-1/4 p-2.5'})
        }
