import pytz
from pytz.exceptions import UnknownTimeZoneError


def tz(request):
    return {'tz_common': pytz.common_timezones}