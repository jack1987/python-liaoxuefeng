import re
from datetime import datetime, timezone, timedelta
import base64
import hashlib
import random
import hmac
import itertools
from urllib import request

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

def login(user, password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    if db[user] == md5.hexdigest():
      return True
    return False
    # 简洁写法
    # return hashlib.md5(password.encode('utf-8')).hexdigest()==db[user]

def login_hmac(username, password):
    #比如500w条数据的彩虹表，用户有40w，在拿到数据库的情况下（也意味着拿到所有的盐），则攻击者需要增加40w*500w的数据,如果只生成一个global的salt，黑客拿到就只用生成500w
    user = db[username]
    return user.password == hmac_md5(user.key, password)

def pi(N):
    ' 计算pi的值 '
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...

    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.

    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...

    # step 4: 求和:
    return sum([(2 - i % 4)/i * 4 for i in itertools.takewhile(lambda x : x<=2*N-1, itertools.count(1,2))])

def fetch_data(url):
    with request.urlopen(url) as f:
        return json.loads(f.read().decode('utf-8'))


if __name__ == '__main__':
    print(pi(100))
