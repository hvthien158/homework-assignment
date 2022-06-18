from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:problem_id>', views.result, name="result"),
    path('problem/', views.problem, name="problem"),
    path('history/', views.history, name="history"),
    path('problem-teacher/', views.problem, name="problem-teacher"),
    path('detail/<int:problem_id>', views.detailProblem.as_view(), name='detail'),
    path('add_problem/', views.AddNewProblem.as_view(), name="add_problem"),
    path('add_question/<int:problem_id>', views.AddListQuestion.as_view(), name="add_question"),
    path('delete/<int:problem_id>', views.deleteProblem, name="delete"),
    path('update/<int:problem_id>', views.updateProblem.as_view(), name="update"),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('', views.Login.as_view(), name='login')
]