from .compat import string_types
from .models import PRIORITY, SMS, STATUS
from .settings import get_default_priority

from collections import defaultdict


def parse_priority(priority):
    if priority is None:
        priority = get_default_priority()
    # If priority is given as a string, returns the enum representation
    if isinstance(priority, string_types):
        priority = getattr(PRIORITY, priority, None)

        if priority is None:
            raise ValueError('Invalid priority, must be one of: %s' %
                             ', '.join(PRIORITY._fields))
    return priority


def split_smss(smss, split_count=1):
    # Group smss into X sublists
    # taken from http://www.garyrobinson.net/2008/04/splitting-a-pyt.html
    if list(smss):
        return [smss[i::split_count] for i in range(split_count)]


def get_sms_usage(start_date, end_date):
    if start_date > end_date:
        raise ValueError('`start` must be earlier than `end`')

    messages = SMS.objects.filter(created__range=[start_date, end_date]).only("status", "backend_alias")

    result_sms_usage = defaultdict(lambda: {"total": 0, "succes": 0, "failed": 0})

    for message in messages:
        result_sms_usage[message.backend_alias]["total"] += 1
        if message.status == STATUS.sent:
            result_sms_usage[message.backend_alias]["succes"] += 1
        else:
            result_sms_usage[message.backend_alias]["failed"] += 1

    return result_sms_usage
