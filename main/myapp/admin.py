from django.contrib import admin
from .models import Question, Problem, History
# Register your models here.

admin.site.register(Problem)
admin.site.register(Question)
admin.site.register(History)