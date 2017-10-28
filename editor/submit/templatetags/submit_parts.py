from django import template

register = template.Library()

@register.filter
def verbose(obj, msg):
    """
    Use to print verbose versions of `constants.JudgeTestResult` or `constants.ReviewResponse`.
    """
    return obj.verbose(msg)

@register.filter
def get_key(value, arg):
    """
    Uset to get value of dictionary. Key is in arg.
    """
    return value[arg]
