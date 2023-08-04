"""
Convert timestamps to defined timezones
especially import for chronic Percept data
"""
from sys import version_info
from datetime import datetime
import zoneinfo
from datetime import timezone

def get_timezones(LOCAL_CITY: str = 'Berlin'):

    if version_info.major >= 3 and version_info.minor >= 9:

        for z in zoneinfo.available_timezones():
            if z.split('/')[-1] == LOCAL_CITY: break
        print(f'Timezone select for local-time: {z}')
        local_tz = zoneinfo.ZoneInfo(z)
        utc = timezone.utc

    else:
        import pytz

        utc = pytz.utc
        local_tz = pytz.timezone(f'Europe/{LOCAL_CITY}')

    return utc, local_tz


def convert_times_to_local(og_times, return_datetime_obj=True,):
    
    

    utc, local_tz = get_timezones()
    time_format = '%Y-%m-%d %H:%M:%S %Z%z'

    local_times = []

    for t in og_times:
        if t[-1] == 'Z': t = t[:-1]
        t = datetime.fromisoformat(t)
        t = t.replace(tzinfo=utc).astimezone(tz=local_tz)
        local_times.append(t.strftime(time_format))

    if return_datetime_obj:
        local_times = convert_times(local_times)
    
    return local_times


def convert_times(string_times):
    """
    Convert strings to datetime objects w/o timezone info
    (for plotting)
    """
    new_times = []

    for t in string_times:

        new_t = f'{t.split(" ")[0]} {t.split(" ")[1]}'

        new_t = datetime.strptime(new_t, '%Y-%m-%d %H:%M:%S')
        new_times.append(new_t)
    
    return new_times