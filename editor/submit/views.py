import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from submit.models import Problem, Row, ActiveProblem, SubmitOutput
from submit import constants
from submit.helpers import write_chunks_to_file
from submit.judge_helpers import (create_submit_and_send_to_judge, parse_protocol)

def index(request):
    return render(request, 'submit/index.html', {})

@login_required(login_url='/submit/login/')
def problems(request):
    user = request.user
    active = ActiveProblem.objects.filter(user=user).first()
    past_problems = []
    active_problem = None
    if active is not None:
        active_problem = Problem.objects.get(pk=active.problem.id)
        past_problems = Problem.objects.filter(order__lt=active_problem.order)
    else:
        past_problems = Problem.objects.all()
    context_dict = {
        'past_problems': past_problems,
        'active_problem': active_problem,
    }
    return render(request, 'submit/problems.html', context_dict)

@login_required(login_url='/submit/login/')
def active_problem(request):
    # TODO: no active problem?
    user = request.user

    active = ActiveProblem.objects.filter(user=user).first()
    if active is None:
        return HttpResponseRedirect('/submit/problems/')
    else:
        active_problem = Problem.objects.get(pk=active.problem.id)
        return HttpResponseRedirect('/submit/problem/%s' % active_problem.id)

@login_required(login_url='/submit/login/')
def problem(request, problem_id):
    user = request.user

    # TODO: no active problem?
    active = ActiveProblem.objects.filter(user=user).first()
    problem = Problem.objects.get(pk=problem_id)
    readonly = True
    if active is not None:
        active_problem = Problem.objects.get(pk=active.problem.id)
        readonly = (active_problem != problem)

    rows = Row.objects.filter(problem=problem, user=user).order_by('order')
    if request.method == 'POST':
        if readonly:
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)

        for row in rows:
            row.content = request.POST.get('row-%s' % row.order)
            row.save()
        if 'save' in request.POST:
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
        elif 'save-submit' in request.POST:
            create_submit_and_send_to_judge(problem, user)
            # TODO: send to judge really
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
    else:
        submits = SubmitOutput.objects.filter(user=user, problem=problem).order_by('-timestamp')
        context_dict = {
            'problem': problem,
            'rows': rows,
            'readonly': readonly,
            'submits': submits,
            'response': constants.ReviewResponse,
        }
        return render(request, 'submit/problem.html', context_dict)

@csrf_exempt
@require_POST
def receive_protocol(request):
    """
    Receive protocol from judge viac POST.
    """
    submit_output_id = request.POST.get('submit_id')
    submit_output = get_object_or_404(SubmitOutput, pk=submit_output_id)
    user = submit_output.user

    active_problem = ActiveProblem.objects.filter(user=user).first()
    if active_problem is None or active_problem.problem != submit_output.problem:
        # nie je to aktivna uloha
        HttpResponse("")

    protocol = request.POST.get('protocol').encode('utf-8')
    write_chunks_to_file(submit_output.protocol_path(), [protocol])

    protocol_data = parse_protocol(submit_output.protocol_path())
    if protocol_data['ready']:
        submit_output.score = protocol_data['score']
        submit_output.status = protocol_data['final_result']
    else:
        submit_output.status = constants.ReviewResponse.PROTOCOL_CORRUPTED
    submit_output.save()

    if submit_output.status == constants.ReviewResponse.OK:
        user = submit_output.user
        problem_order = submit_output.problem.order
        # TODO: uz nie je dalsi?
        next_problem = Problem.objects.filter(order__gt = problem_order).first()
        if next_problem is not None:
            active_problem.problem = next_problem
            active_problem.save()
        else:
            active_problem.delete()

    return HttpResponse("")


@login_required
def view_submit(request, submit_id):
    submit = get_object_or_404(SubmitOutput, pk=submit_id)
    is_staff = request.user.is_staff

    if submit.user != request.user and not is_staff:
        raise PermissionDenied()

    context_dict = {
        'submit': submit,
    }

    with open(submit.file_path(), 'rb') as submitted_file:
        context_dict['submitted_file'] = submitted_file.read().decode('utf-8', 'replace')

    if submit.protocol_exists():
        force_show_details = is_staff
        context_dict['protocol'] = parse_protocol(submit.protocol_path(), force_show_details)
        context_dict['result'] = constants.JudgeTestResult

    return render(request, 'submit/view_submit.html', context_dict)


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
