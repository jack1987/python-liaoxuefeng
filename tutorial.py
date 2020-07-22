import re
from datetime import datetime, timezone, timedelta

def to_timestamp(dt_str, tz_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    m = re.match(r'^UTC(\+|-)(\d+):(\d+)$', tz_str)
    s = m.group(2)
    if s[0] == '0':
      s = s[1:]
    print(s)
    if m.group(1) == '-':
      tz = timezone(timedelta(hours=-int(s)))
    else:
      tz = timezone(timedelta(hours=int(s)))
    dt = dt.replace(tzinfo = tz)
    return dt.timestamp()
