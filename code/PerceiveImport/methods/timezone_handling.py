"""
Convert timestamps to defined timezones
especially import for chronic Percept data
"""


def get_timezones(LOCAL_CITY: str = 'Berlin'):

    from sys import version_info
    if version_info.major >= 3 and version_info.minor >= 9:
        import zoneinfo
        from datetime import timezone

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


def convert_times_to_local(og_times):
    
    from datetime import datetime

    utc, local_tz = get_timezones()
    time_format = '%Y-%m-%d %H:%M:%S %Z%z'

    local_times = []

    for t in og_times:
        if t[-1] == 'Z': t = t[:-1]
        t = datetime.fromisoformat(t)
        t = t.replace(tzinfo=utc).astimezone(tz=local_tz)
        local_times.append(t.strftime(time_format))
    
    return local_times