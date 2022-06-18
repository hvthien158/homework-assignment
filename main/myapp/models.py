from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Problem(models.Model):
    name = models.CharField(max_length=255, default="no name")
    deadline = models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return self.name


class Question(models.Model):
    answer_choice = ((0, 'A'), (1, 'B'), (2, 'C'), (3, 'D'))
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=1000)
    choice_A = models.CharField(max_length=255)
    choice_B = models.CharField(max_length=255)
    choice_C = models.CharField(max_length=255)
    choice_D = models.CharField(max_length=255)
    answer = models.IntegerField(choices=answer_choice, default=0)

class History(models.Model):
    user = models.CharField(max_length=255)
    problem = models.IntegerField(default=0)
    problem_name = models.CharField(max_length=255, default='')
    score = models.FloatField()
    submit_time = models.DateTimeField(default=timezone.datetime.now())
