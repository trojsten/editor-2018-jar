import os
import socket
import time
import xml.etree.ElementTree as ET
from decimal import Decimal

from django.conf import settings as django_settings

from unidecode import unidecode
import json

from submit.constants import JudgeTestResult, ReviewResponse
from submit.models import SubmitOutput, Row, Task
from submit.helpers import (write_chunks_to_file, write_lines_to_file)
from submit.constants import ReviewResponse


class JudgeConnectionError(Exception):
    pass


def create_submit_and_send_to_judge(problem, user, custom=False):
    submit = SubmitOutput(user=user, problem=problem, score=0, custom=custom, status=ReviewResponse.SENDING_TO_JUDGE)
    submit.save()
    _prepare_raw_file(submit, custom)
    try:
        _send_to_judge(submit)
        submit.status = ReviewResponse.SENT_TO_JUDGE
    except JudgeConnectionError:
        submit.status = ReviewResponse.JUDGE_UNAVAILABLE
        raise JudgeConnectionError
    finally:
        submit.save()

def _send_to_judge(submit):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((django_settings.JUDGE_ADDRESS, django_settings.JUDGE_PORT))
        with open(submit.raw_path(), 'rb') as raw:
            sock.send(raw.read())
    except:
        raise JudgeConnectionError
    finally:
        sock.close()

def _prepare_raw_file(submit, custom):
    rows = Row.objects.filter(user=submit.user, problem=submit.problem).order_by('order')
    custom_input = Task.objects.get(user=submit.user, problem=submit.problem).custom_input

    submit_id = str(submit.id)
    user_id = '%s-%s' % (django_settings.JUDGE_INTERFACE_IDENTITY, str(submit.user.id))

    timestamp = int(time.time())

    custom_input_json = json.loads('{ %s }' % custom_input) if custom else ''

    info = {
        'judge': django_settings.JUDGE_INTERFACE_IDENTITY,
        'submit_id': submit_id,
        'user_id': user_id,
        'timestamp': timestamp,
        'problem': submit.problem.id,
        'code': [(row.content, row.get_lang_display()) for row in rows],
        'custom': custom,
        'custom_input': custom_input_json,
    }

    # write because of code in submit view
    write_lines_to_file(submit.file_path(), [row.content for row in rows])
    write_lines_to_file(submit.lang_path(), [row.get_lang_display() for row in rows])
    if custom:
        write_lines_to_file(submit.custom_input_path(), custom_input.split('\n'))
    with open(submit.raw_path(), 'w') as outfile:
       json.dump(info, outfile)

def parse_protocol(protocol_path, force_show_details=False):
    """
    Reads a testing protocol and prepares context for a web page rendering the protocol.
    """
    data = dict()
    data['ready'] = True

    try:
        tree = ET.parse(protocol_path)
    except:
        # Protocol is either corrupted or just upload is not finished
        data['ready'] = False
        return data

    clog = tree.find('compileLog')
    data['compile_log_present'] = clog is not None
    data['compile_log'] = clog.text if clog is not None else ''
    clog_line = tree.find('cLogLineNumber')
    data['compile_log_line'] = int(clog_line.text) if clog_line is not None else None

    tests = []
    runlog = tree.find('runLog')
    if runlog is not None:
        for runtest in runlog:
            # Test log format in protocol is: name, resultMsg, line, details
            if runtest.tag != 'test':
                continue
            test = dict()
            test['name'] = runtest[0].text
            test['result'] = runtest[1].text
            test['line'] = int(runtest[2].text)
            details = runtest[3].text if len(runtest) > 3 else None
            test['details'] = details
            test['show_details'] = details is not None and ('sample' in test['name'] or 'custom' in test['name'] or  force_show_details)
            tests.append(test)
    data['tests'] = sorted(tests, key=lambda test: test['name'])
    data['have_tests'] = len(tests) > 0

    try:
        data['score'] = Decimal(tree.find('runLog/score').text)
    except:
        data['score'] = 0

    if data['compile_log_present']:
        data['final_result'] = JudgeTestResult.COMPILATION_ERROR
    else:
        # Test result of review is set by first non-OK test result
        data['final_result'] = JudgeTestResult.OK
        if not data['have_tests']:
            data['final_result'] = ReviewResponse.PROTOCOL_CORRUPTED
        for test in data['tests']:
            if test['result'] != JudgeTestResult.OK:
                data['final_result'] = test['result']
                break

    return data
