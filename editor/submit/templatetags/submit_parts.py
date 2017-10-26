from django import template

register = template.Library()

@register.filter
def verbose(obj, msg):
    """
    Use to print verbose versions of `constants.JudgeTestResult` or `constants.ReviewResponse`.
    """
    return obj.verbose(msg)
