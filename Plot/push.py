# @Author  : JL
# @Time    : 2016/8/14 11:44
import json

import jpush
from jpush import common

from fund.FundInv import Inverst

_jpush = jpush.JPush("1af8ad4679605e3b54646a14", "e2de3660a168fdf96f098f40")
push = _jpush.create_push()
# if you set the logging level to "DEBUG",it will show the debug logging.
_jpush.set_logging("DEBUG")
push.audience = jpush.all_
push.platform = jpush.all_


def send(message, alert):
    android_msg = jpush.android(alert=alert)
    push.notification = jpush.notification(alert=message, android=android_msg)
    try:
        response = push.send()
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn error")
    except common.JPushFailure:
        print("JPushFailure")
    except:
        print("Exception")


list = []
list.append({"code": "160119", "amount": 10005})
list.append({"code": "160119", "amount": 10005})
list.append({"code": "160119", "amount": 10005})
# list.append(Inverst("160119", 10500,0))
# list.append(Inverst("160630", 10500))
# list.append(Inverst("160630", 10500))
# list.append(Inverst("160630", 10500.0))
send("购买基金", json.dumps(list, default=lambda obj: obj.__dict__))
