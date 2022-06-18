from django.forms import ModelForm
from . import models

class ProblemForm(ModelForm):
    class Meta:
        model = models.Problem
        fields = ['name','deadline']

class QuestionForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ['question_text', 'choice_A', 'choice_B', 'choice_C', 'choice_D', 'answer']