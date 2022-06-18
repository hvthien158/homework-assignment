from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from .models import Question, Problem, History
from django.views import View
from django.contrib.auth import authenticate, login, decorators, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from . import forms
# Create your views here.


class Login(View):
    def get(self, request):
        logout(request)
        p = Problem.objects.all()

        # Auto delete problem that is over deadline
        for item in p:
            if item.deadline is not None:
                if item.deadline < timezone.now():
                    Problem.objects.filter(id=item.id).delete()
        return render(request, 'myapp/login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        check = authenticate(username=username, password=password)
        if check is None:
            return render(request, 'myapp/login.html', {"check" : False})
        else:
            login(request, check)
            return HttpResponsePermanentRedirect("/problem")

@decorators.login_required(login_url='/')
def problem(request):
    listProblem = Problem.objects.all()
    listHitory = History.objects.all()
    list = []
    for item in listProblem:
        list.append(item)
        for item2 in listHitory:
            if item.id == item2.problem and request.user.get_username() == item2.user:
                list.remove(item)
                break
    newest = []
    if len(list) >= 3:
        for i in range(len(list) - 1, len(list) - 4, -1):
            newest.append(list[i])
    else:
        for i in range(len(list) - 1, -1, -1):
            newest.append(list[i])
    context = {"list": list, "new" : newest, "i": 1}
    if request.user.has_perm('myapp.add_problem') and request.user.has_perm('myapp.delete_problem') and request.user.has_perm('myapp.change_problem'):
        return render(request, 'myapp/problem-teacher.html', context)
    else:
        return render(request, 'myapp/problem.html', context)

class detailProblem(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, problem_id):
        p = Problem.objects.get(pk=problem_id)
        return render(request, 'myapp/detailProblem.html', {"p": p})

@decorators.login_required(login_url='/')
def history(request):
    listHitory = History.objects.all()
    list = []
    for item in listHitory:
        if request.user.get_username() == item.user:
            list.append(item)
    return render(request, 'myapp/history.html', {'history' : list})

@decorators.login_required(login_url='/')
def result(request, problem_id):
    p = Problem.objects.get(pk=problem_id)
    dl = []

    for item in p.question_set.all():
        template = "choice_" + str(item.id)
        print(item.answer, ord(request.GET[template]) - 65)
        dl.append(str(item.answer) == str(ord(request.GET[template]) - 65))

    num = dl.count(True)
    sum = len(dl)
    kq = num * 100 / sum

    username = request.user.get_username()
    h = History(user=username, problem=problem_id,problem_name=p.name , score=kq, submit_time=timezone.datetime.now())
    h.save()

    return render(request, 'myapp/result.html', {"num" : num, "sum" : sum, "kq" : kq})

class AddNewProblem(View):
    def get(self, request):
        listProblem = Problem.objects.all()
        f = forms.ProblemForm
        context = {'form' : f, 'list' : listProblem}
        return render(request, 'myapp/add_problem.html', context)
    def post(self, request):
        f = forms.ProblemForm(request.POST)
        if request.user.has_perm('myapp.add_problem'):
            f.save()
            direct = '/add_question/' + str(f.instance.id)
            return HttpResponsePermanentRedirect(direct)
        else:
            return HttpResponse('Tài khoãn của bạn không có quyền này')

class AddListQuestion(View):
    def get(self, request, problem_id):
        listProblem = Problem.objects.all()
        f = forms.QuestionForm
        context = {'form': f, 'list' : listProblem}
        return render(request, 'myapp/add_question.html', context)
    def post(self, request, problem_id):
        f = forms.QuestionForm(request.POST)
        if request.user.has_perm('myapp.add_question'):
            f.instance.problem = Problem.objects.get(pk=problem_id)
            f.save()
            if(request.POST.get('new') is not None):
                listProblem = Problem.objects.all()
                fn = forms.QuestionForm
                context = {'form': fn, 'list' : listProblem}
                return render(request, 'myapp/add_question.html', context)
            else:
                return HttpResponsePermanentRedirect('/problem')
        else:
            return HttpResponse('Tài khoãn của bạn không có quyền này')

@decorators.login_required(login_url='/')
def deleteProblem(request, problem_id):
    if request.user.has_perm('myapp.delete_problem'):
        Problem.objects.filter(id=problem_id).delete()
        return HttpResponsePermanentRedirect("/problem")
    else:
        return HttpResponse('Tài khoản của bạn không có quyền này')

class updateProblem(View):
    login_url = '/'
    def get(self, request, problem_id):
        listProblem = Problem.objects.all()
        problem = Problem.objects.get(pk=problem_id)
        return render(request, 'myapp/update.html', {"problem" : problem, 'list' : listProblem})

    def post(self, request, problem_id):
        problem = Problem.objects.get(pk=problem_id)
        list_question = Question.objects.filter(problem=problem)
        for item in list_question:
            item.question_text = request.POST.get('question_text_' + str(item.id))
            item.choice_A = request.POST.get('choice_A_' + str(item.id))
            item.choice_B = request.POST.get('choice_B_' + str(item.id))
            item.choice_C = request.POST.get('choice_C_' + str(item.id))
            item.choice_D = request.POST.get('choice_D_' + str(item.id))
            item.answer = request.POST.get('answer_' + str(item.id))
            item.save()
        problem.name = request.POST.get('problem_name')
        problem.deadline = request.POST.get('problem_deadline')
        problem.save()
        return HttpResponse('Success')

@decorators.login_required(login_url='/')
def logout_user(request):
    logout(request)
    return HttpResponsePermanentRedirect('/')