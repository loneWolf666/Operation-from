import time
import uuid


def make_uid():
    num = str(int(uuid.uuid1()))[:5]
    date = str(round(time.time() * 1000))
    uid = ''.join([date, num])
    return uid