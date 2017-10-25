from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from submit.models import Problem, Row
import sys

def index(request):
    return render(request, 'submit/index.html', {})

@login_required(login_url='/submit/login/')
def problems(request):
    all_entries = Problem.objects.order_by('order')
    # TODO: filter only those which he can see
    context_dict = {
        'problems': all_entries
    }
    return render(request, 'submit/problems.html', context_dict)

@login_required(login_url='/submit/login/')
def problem(request, problem_id):
    user = request.user
    problem = Problem.objects.get(pk=problem_id)
    rows = Row.objects.filter(problem=problem, user=user).order_by('order')
    if request.method == 'POST':
        for row in rows:
            row.content = request.POST.get('row-%s' % row.order)
            row.save()
        if 'save' in request.POST:
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
        elif 'save-submit' in request.POST:
            # TODO: add testing
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
    else:
        context_dict = {
            'problem': problem,
            'rows': rows,
        }
        return render(request, 'submit/problem.html', context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/submit/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'submit/login.html', {})

@login_required(login_url='/submit/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/submit/')


# Create your views here.
