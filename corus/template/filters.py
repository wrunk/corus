"""Coffin automatically makes Django's builtin filters available in Jinja2,
through an interop-layer.

However, Jinja 2 provides room to improve the syntax of some of the
filters. Those can be overridden here.

TODO: Most of the filters in here need to be updated for autoescaping.
"""
import types

from jinja2.runtime import Undefined
from jinja2 import filters, Markup

from django.utils.html import escapejs as django_escapejs


def active(request, pattern):
    if pattern == '':
        if request.path == '/':
            return 'active'
        else:
            return ''
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''


def timesince(value, *arg):
    if value is None or isinstance(value, Undefined):
        return u''
    from django.utils.timesince import timesince
    return timesince(value, *arg)


def timeuntil(value, *args):
    if value is None or isinstance(value, Undefined):
        return u''
    from django.utils.timesince import timeuntil
    return timeuntil(value, *args)


def date(value, arg=None):
    """Formats a date according to the given format."""
    if value is None or isinstance(value, Undefined):
        return u''
    from django.conf import settings
    from django.utils import formats
    from django.utils.dateformat import format
    if arg is None:
        arg = settings.DATE_FORMAT
    try: 
        return formats.date_format(value, arg) 
    except AttributeError:
        try: 
            return format(value, arg) 
        except AttributeError:
            return ''


def time(value, arg=None):
    """Formats a time according to the given format."""
    if value is None or isinstance(value, Undefined):
        return u''
    from django.conf import settings
    from django.utils import formats
    from django.utils.dateformat import time_format
    if arg is None:
        arg = settings.TIME_FORMAT
    try: 
        return formats.time_format(value, arg) 
    except AttributeError:
        try: 
            return time_format(value, arg) 
        except AttributeError:
            return ''


def truncatewords(value, length):
    # Jinja2 has it's own ``truncate`` filter that supports word
    # boundaries and more stuff, but cannot deal with HTML.
    try:
        from django.utils.text import Truncator
    except ImportError:
        from django.utils.text import truncate_words # Django < 1.6
    else:
        truncate_words = lambda value, length: Truncator(value).words(length)
    return truncate_words(value, int(length))


def truncatewords_html(value, length):
    try:
        from django.utils.text import Truncator
    except ImportError:
        from django.utils.text import truncate_html_words # Django < 1.6
    else:
        truncate_html_words = lambda value, length: Truncator(value).words(length, html=True)
    return truncate_html_words(value, int(length))


def pluralize(value, s1='s', s2=None):
    """Like Django's pluralize-filter, but instead of using an optional
    comma to separate singular and plural suffixes, it uses two distinct
    parameters.

    It also is less forgiving if applied to values that do not allow
    making a decision between singular and plural.
    """
    if s2 is not None:
        singular_suffix, plural_suffix = s1, s2
    else:
        plural_suffix = s1
        singular_suffix = ''

    try:
        if int(value) != 1:
            return plural_suffix
    except TypeError: # not a string or a number; maybe it's a list?
        if len(value) != 1:
            return plural_suffix
    return singular_suffix


def escapejs(value):
    """
    A Jinja2 filter for escaping javascript. Same as django's but
    quotes returned values in order to handle None values correctly.
    """
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return Markup(str(value).lower())
    if isinstance(value, (types.IntType, types.LongType, types.FloatType)):
        return Markup(value)
    return Markup('"{}"'.format(django_escapejs(value)))


def default(value, default_value=u'', boolean=True):
    """Make the default filter, if used without arguments, behave like
    Django's own version.
    """
    return filters.do_default(value, default_value, boolean)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"