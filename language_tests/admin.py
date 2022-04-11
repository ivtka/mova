from django.contrib import admin

from language_tests.models import Language, Level, Question, Result

admin.site.register(Language)
admin.site.register(Level)
admin.site.register(Question)
admin.site.register(Result)
