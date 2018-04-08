from django.utils.translation import ugettext_lazy as _

SUBMITTED_FILE_EXTENSION = '.submit'
SUBMITTED_CUSTOM_INPUT_FILE_EXTENSION = '.custom'
SUBMITTED_LANG_FILE_EXTENSION = '.langs'
TESTING_PROTOCOL_EXTENSION = '.protocol'
TESTING_RAW_EXTENSION = '.raw'

class JudgeTestResult(object):
    """
    Groups all common values of test results in protocol.
    Stores verbose versions of results.
    """
    OK = 'OK'
    WRONG_ANSWER = 'WA'
    TIME_LIMIT_EXCEEDED = 'TLE'
    RUNTIME_EXCEPTION = 'EXC'
    SECURITY_EXCEPTION = 'SEC'
    IGNORED = 'IGN'
    COMPILATION_ERROR = 'CERR'
    DONE = 'DONE'

    VERBOSE_RESULT = {
        OK: _('OK'),
        WRONG_ANSWER: _('Wrong answer'),
        TIME_LIMIT_EXCEEDED: _('Time limit exceeded'),
        RUNTIME_EXCEPTION: _('Runtime exception'),
        SECURITY_EXCEPTION: _('Security exception'),
        IGNORED: _('Ignored'),
        COMPILATION_ERROR: _('Compilation error'),
        DONE: _('Done'),
    }

    @classmethod
    def verbose(cls, result):
        return cls.VERBOSE_RESULT.get(result, result)


class ReviewResponse(JudgeTestResult):
    """
    Groups all common values of Review.short_response.
    Stores verbose versions of responses.
    """

    SENDING_TO_JUDGE = 'Sending to judge'
    SENT_TO_JUDGE = 'Sent to judge'
    JUDGE_UNAVAILABLE = 'Judge unavailable'
    PROTOCOL_CORRUPTED = 'Protocol corrupted'
    REVIEWED = 'Reviewed'

    VERBOSE_RESPONSE = {
        # strings are as literals here so `manage.py makemessages` will include them into django.po file
        SENDING_TO_JUDGE: _('Sending to judge'),
        SENT_TO_JUDGE: _('Sent to judge'),
        JUDGE_UNAVAILABLE: _('Judge unavailable'),
        PROTOCOL_CORRUPTED: _('Protocol corrupted'),
        REVIEWED: _('Reviewed'),
    }

    @classmethod
    def verbose(cls, response):
        if response in cls.VERBOSE_RESPONSE:
            return cls.VERBOSE_RESPONSE[response]
        return cls.VERBOSE_RESULT.get(response, response)

    @classmethod
    def all_items_as_choices(cls):
        judge_responses = list(cls.VERBOSE_RESULT.items())
        communication = [(k, v) for k, v in cls.VERBOSE_RESPONSE.items() if k != ReviewResponse.REVIEWED]
        manual = ((ReviewResponse.REVIEWED, cls.verbose(ReviewResponse.REVIEWED)), )

        choices = (
            (_('Manual review'), manual),
            (_('Judge test results'), judge_responses),
            (_('Judge communication'), communication),
        )

        return choices

class Language(object):
    CPP = 1
    PYTHON = 2
    FREE_PASCAL = 3
    GO = 4
    PHP = 5
    RUST = 6
    PERL = 7
    R = 8
    LANG_CHOICES = (
            (CPP, 'C++'),
            (PYTHON, 'Python'),
            (FREE_PASCAL, 'FreePascal'),
            (GO, 'Go'),
            (PHP, 'PHP'),
            (RUST, 'Rust'),
            (PERL, 'Perl'),
            (R, 'R'),
    )
