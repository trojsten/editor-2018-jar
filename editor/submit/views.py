from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from submit.models import Problem

def index(request):
    return render(request, 'submit/index.html', {})

@login_required
def problems(request):
    all_entries = Problem.objects.order_by('order')
    # TODO: filter only those which he can see
    context_dict = {'problems': all_entries}
    return render(request, 'submit/problems.html', context_dict)

@login_required
def problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    return render(request, 'submit/problem.html', {'problem': problem})

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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/submit/')


# Create your views here.
