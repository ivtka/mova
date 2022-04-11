from django.db import models

from django.contrib.auth.models import User

class Language(models.Model):
    language_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.language_name


class Level(models.Model):
    LEVELS = (('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'),
              ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2'))
    level = models.CharField(unique=True, max_length=2, choices=LEVELS)


class Question(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    OPTIONS = (('Option1', 'Option1'), ('Option2', 'Option2'),
               ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=OPTIONS)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
