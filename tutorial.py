import re
from datetime import datetime, timezone, timedelta
import base64

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

def safe_base64_decode(s):
    # s = 'YWJjZA==' or 'YWJjZA'
    # len(s)%4 will be 3, since Base64 convert 3bytes to 4bytes, if original binary is 1 byte, Base64 will be 1%(4/3) bytes, pad 0 to 2 bytes
    # same for 2 bytes -> base64 3bytes
    if len(s)%4 == 0:
        return base64.b64decode(s)
    else:
        s = s + len(s) % 4 * b'='
        return base64.b64decode(s)

def bmp_info(data):
    # big endian for OS
    # little endian for network protocol
    t = struct.unpack('<ccIIIIIIHH', data[:30])
    return {
        'width': t[6],
        'height':t[7],
        'color': t[9]
    }
