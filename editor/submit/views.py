import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from submit.models import Problem, Row, ActiveProblem, SubmitOutput, SpareRow, CustomInput
from submit import constants
from submit.helpers import write_chunks_to_file
from submit.judge_helpers import (create_submit_and_send_to_judge, parse_protocol)

def index(request):
    return render(request, 'submit/index.html', {})

def create_active_if_first_login(user):
    problems = Problem.objects.all()
    first = problems.first()

    active_problem = ActiveProblem.objects.filter(user=user).first()
    if active_problem is not None:
        return {
            'error': None,
            'active_problem': active_problem,
            'no_more_problems': False,
        }

    error = None
    active_problem = None
    no_more_problems = False
    if first is None:
        # ziadne ulohy ani nie su?
        error = "Neexistujú žiadne úlohy!"
    else:
        last_ok_submit = SubmitOutput.objects.filter(
                user=user, problem=first, status=constants.ReviewResponse.OK).last()
        if last_ok_submit is None:
            # Ak je to prvy krat, mozno sme im zabudli nastavit prvy aktivny problem.
            # este nesubmitli nic ani k prvej ulohe
            active_problem = ActiveProblem.objects.create(user=user, problem=first)
            custom_input = CustomInput.objects.create(user=user, problem=first)
        else:
            # kedze nemaju aktivny problem, ale maju submit k prvemu, tak skoncili
            no_more_problems = True
    return {
        'error': error,
        'active_problem': active_problem,
        'no_more_problems': no_more_problems,
    }

@login_required(login_url='/submit/login/')
def problems(request):
    user = request.user

    result = create_active_if_first_login(user)

    past_problems = []
    active_problem = result['active_problem']
    error = result['error']
    no_more_problems = result['no_more_problems']
    problem = None
    if no_more_problems:
        past_problems = Problem.objects.all()
    elif active_problem is not None:
        problem = Problem.objects.get(pk=active_problem.problem.id)
        past_problems = Problem.objects.filter(order__lt=problem.order)
    context_dict = {
        'past_problems': past_problems,
        'active_problem': problem,
        'error': error,
        'no_more_problems': no_more_problems,
    }
    return render(request, 'submit/problems.html', context_dict)

@login_required(login_url='/submit/login/')
@require_POST
def add_lang_row(request, problem_id, lang_code):
    user = request.user

    active_problem = ActiveProblem.objects.filter(user=user).first()
    if active_problem is None or int(active_problem.problem.id) != int(problem_id):
        return HttpResponseRedirect('/submit/problem/%s' % problem_id)

    spare_row = SpareRow.objects.filter(user=user, lang=lang_code).first()
    if spare_row is None:
        # nemaju taky riadok
        return HttpResponseRedirect('/submit/problem/%s' % problem_id)

    problem = active_problem.problem
    row = Row.objects.filter(user=user, problem=problem).order_by('order').last()
    new_order = 1
    if row is not None:
        new_order = row.order + 1
    Row.objects.create(
            user=user,
            problem=problem,
            order=new_order,
            lang=lang_code,
            content="")
    spare_row.delete()
    return HttpResponseRedirect('/submit/problem/%s' % problem_id)

@login_required(login_url='/submit/login/')
def problem(request, problem_id):
    user = request.user

    result = create_active_if_first_login(user)
    if result['error'] is not None:
        return HttpResponseRedirect('/submit/problems/')

    readonly = True
    problem = Problem.objects.get(pk=problem_id)
    if result['no_more_problems']:
        readonly = True
    else:
        # active problem existuje
        active = result['active_problem']
        active_problem = Problem.objects.get(pk=active.problem.id)
        readonly = (active_problem != problem)

        if problem.order > active_problem.order:
            return HttpResponseRedirect('/submit/problems/')

    rows = Row.objects.filter(problem=problem, user=user).order_by('order')
    if request.method == 'POST':
        # Save everytime, because we are redirecting everytinme.
        if readonly:
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)

        for row in rows:
            row.content = request.POST.get('row-%s' % row.order)
            row.save()
        custom_input = CustomInput.objects.get(user=user, problem=problem)
        custom_input.content = request.POST.get('custom-input')
        custom_input.save()

        if 'save' in request.POST:
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
        elif 'save-submit' in request.POST:
            create_submit_and_send_to_judge(problem, user)
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
        elif 'save-custom-run' in request.POST:
            create_submit_and_send_to_judge(problem, user, custom=True)
            return HttpResponseRedirect('/submit/problem/%s' % problem_id)
    else:
        submits = SubmitOutput.objects.filter(user=user, problem=problem).order_by('-timestamp')
        lang_counts = SpareRow.objects.filter(user=user).values('lang').annotate(num_rows=Count('lang')).order_by('-num_rows')
        custom_input = CustomInput.objects.get(user=user, problem=problem)
        context_dict = {
            'problem': problem,
            'rows': rows,
            'readonly': readonly,
            'submits': submits,
            'lang_counts': lang_counts,
            'lang_codes': { code: name for code,name in constants.Language.LANG_CHOICES },
            'custom_input': custom_input,
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
        next_problem = Problem.objects.filter(order__gt = problem_order).first()
        if next_problem is not None:
            active_problem.problem = next_problem
            active_problem.save()
            CustomInput.objects.get_or_create(user=user, problem=next_problem)
        else:
            # uz nei je dalsi problem
            active_problem.delete()

    return HttpResponse("")


@login_required(login_url='/submit/login/')
def view_submit(request, submit_id):
    submit = get_object_or_404(SubmitOutput, pk=submit_id)
    is_staff = request.user.is_staff

    if submit.user != request.user and not is_staff:
        raise PermissionDenied()

    context_dict = {
        'submit': submit,
    }

    with open(submit.file_path(), 'rb') as submitted_file:
        sub_file = submitted_file.read().decode('utf-8', 'replace')
        with open(submit.lang_path(), 'rb') as lang_file:
            file = lang_file.read().decode('utf-8', 'replace')
            order = 1
            rows = []
            for content_line, lang_line in zip(sub_file.split('\n')[:-1], file.split('\n')[:-1]):
                rows.append({
                    'content': content_line,
                    'order': order,
                    'lang': lang_line,
                    })
                order += 1
            context_dict['rows'] = rows

    if submit.protocol_exists():
        force_show_details = is_staff
        context_dict['protocol'] = parse_protocol(submit.protocol_path(), force_show_details)
        context_dict['result'] = constants.JudgeTestResult
    if submit.custom:
        with open(submit.custom_input_path(), 'r') as inp:
            context_dict['custom_input'] = inp.read()

    return render(request, 'submit/view_submit.html', context_dict)

@login_required(login_url='/submit/login/')
@staff_member_required
def add_row_info(request, user_id):
    user = User.objects.get(pk=user_id)
    active_problem = ActiveProblem.objects.filter(user=user).first()
    if active_problem is None:
        return JsonResponse({'no_active_problem': True});
    problem = active_problem.problem
    row = Row.objects.filter(user=user, problem=problem).last()
    next_order = 1
    if row is not None:
        next_order = row.order + 1
    return JsonResponse({
        'no_active_problem': False,
        'problem_id': problem.id,
        'problem_title': problem.title,
        'next_order': next_order,
    })

@login_required(login_url='/submit/login/')
@staff_member_required
def add_spare_rows(request):
    if request.method == 'POST':
        user_id = request.POST.get('user-select')
        user = User.objects.get(pk=user_id)
        langs = constants.Language.LANG_CHOICES
        for number, lang in langs:
            count = request.POST.get('lang-input-%s' % number)
            count = 0 if count == '' else int(count)
            for i in range(count):
                SpareRow.objects.create(user=user, lang=number)
        return HttpResponseRedirect('/submit/add_spare_rows/')
    else:
        users = User.objects.all()
        langs = constants.Language.LANG_CHOICES

        n = len(langs)
        k1, k2, k3 = n//3 + (n%3 == 1), n//3 + (n%3 == 2), n//3

        context_dict = {
            'users': users,
            'langs': langs,
            'lang_groups': [langs[:k1],langs[k1:k1+k2],langs[k1+k2:]],
        }
        return render(request, 'submit/add_spare_rows.html', context_dict)

@login_required(login_url='/submit/login/')
@staff_member_required
def view_results(request):
    users = User.objects.all()
    problems = Problem.objects.all().order_by('order')

    results = {}
    count_oks = {}
    for user in users:
        user_results = {}
        count_ok = 0
        for problem in problems:
            last_submit = SubmitOutput.objects.filter(
                    user=user, problem=problem).exclude(status=constants.ReviewResponse.DONE).order_by('timestamp').last()
            last_ok_submit = SubmitOutput.objects.filter(
                    user=user, problem=problem,
                    status=constants.ReviewResponse.OK).order_by('timestamp').last()
            if last_ok_submit is None:
                user_results[problem.id] = last_submit
            else:
                user_results[problem.id] = last_ok_submit
                count_ok += 1
        results[user.id] = user_results
        count_oks[user.id] = count_ok

    context_dict = {
        'users': users,
        'problems': problems,
        'results': results,
        'count_oks': count_oks,
        'response': constants.ReviewResponse,
    }
    return render(request, 'submit/view_results.html', context_dict)

def work_after_login(user):
    result = create_active_if_first_login(user)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                work_after_login(user)
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
