import os
import socket
import time
import xml.etree.ElementTree as ET
from decimal import Decimal

from django.conf import settings as django_settings

from unidecode import unidecode

from submit.constants import JudgeTestResult, ReviewResponse
from submit.models import SubmitOutput, Row
from submit.helpers import (write_chunks_to_file, write_lines_to_file)
from submit.constants import ReviewResponse


class JudgeConnectionError(Exception):
    pass


def create_submit_and_send_to_judge(problem, user):
    submit = SubmitOutput(user=user, problem=problem, score=0, status=ReviewResponse.SENDING_TO_JUDGE)
    submit.save()
    _prepare_raw_file(submit)
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

def _prepare_raw_file(submit):
    # TODO: send languages info, not only code
    rows = Row.objects.filter(user=submit.user, problem=submit.problem).order_by('order')
    write_lines_to_file(submit.file_path(), [row.content for row in rows])
    with open(submit.file_path(), 'rb') as submitted_file:
        submitted_source = submitted_file.read()

        submit_id = str(submit.id)
        user_id = '%s-%s' % (django_settings.JUDGE_INTERFACE_IDENTITY, str(submit.user.id))

        timestamp = int(time.time())

        raw_head = "%s\n%s\n%s\n%s\n%d\n%s\n" % (
            django_settings.JUDGE_INTERFACE_IDENTITY,
            submit_id,      # judge expects submit_id, but at front-end it is Review that stores all feedback data
            user_id,
            '', # correct_filename,
            timestamp,
            '', #original_filename,
        )

        write_chunks_to_file(submit.raw_path(), [raw_head.encode('UTF-8'), submitted_source])


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

    tests = []
    runlog = tree.find('runLog')
    if runlog is not None:
        for runtest in runlog:
            # Test log format in protocol is: name, resultCode, resultMsg, time, details
            if runtest.tag != 'test':
                continue
            test = dict()
            test['name'] = runtest[0].text
            test['result'] = runtest[2].text
            test['time'] = runtest[3].text
            details = runtest[4].text if len(runtest) > 4 else None
            test['details'] = details
            test['show_details'] = details is not None and ('sample' in test['name'] or force_show_details)
            tests.append(test)
    data['tests'] = tests
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
        for test in data['tests']:
            if test['result'] != JudgeTestResult.OK:
                data['final_result'] = test['result']
                break

    return data
