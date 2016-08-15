# encoding:UTF-8
import gzip
import http.cookiejar
import json
import logging
import socket
import traceback
import urllib.parse
import urllib.request
from datetime import datetime
from http.client import RemoteDisconnected, IncompleteRead
from urllib.error import HTTPError, URLError

socket.setdefaulttimeout(20)
from functools import partial, wraps


# 使用内嵌包装函数来确保每次新函数都被调用，
# 内嵌包装函数的形参和返回值与原函数相同，装饰函数返回内嵌包装函数对象
def safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (HTTPError, URLError) as error:
            logging.error('URL: %s not retrieved because %s', args[0], error)
            #except：捕捉错误是为了记录且不中断程序
            #raise：由于底层函数，不知道如何处理该错误，所以，最恰当的方式是继续往上抛，让顶层调用者去处理
            raise
        except socket.timeout as error:
            logging.error('URL: %s not retrieved because %s', args[0], error)
            raise
        except ConnectionAbortedError as error:
            logging.error('URL: %s not retrieved because %s', args[0], error)
            raise
        except IncompleteRead as error:
            logging.error('URL: %s not retrieved because %s', args[0], error)
            raise
        except RemoteDisconnected as  error:
            logging.error('URL: %s not retrieved because %s', args[0], error)
            raise
        except Exception:
            traceback.print_exc()
            raise
        else:
            pass

    return wrapper


__opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
__opener.addheaders = [("User-agent",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"),
                       ("Cache-control", "max-age=0"),
                       ("Connection", "keep-alive"),
                       ("Accept", "*/*")
                       ]
encoding = "utf-8"


# 参数类型：Form Data/Body
@safe
def postForm(url, params):
    # urlencode对dict编码加入url
    # urlencode只接受dict类型的
    postData = urllib.parse.urlencode(params)
    # 第二个参数不管post携带form data还是json，都需要经过encode()编码过才能提交
    resp = __opener.open(url, postData.encode()).read().decode(encoding)


def auto_decode(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        __encoding__ = resp.headers.get('Content-Encoding')
        doc = resp.read()
        html = ""
        if __encoding__ == "gzip":
            # 解码
            html = gzip.decompress(doc).decode(encoding)
        elif __encoding__:
            html = doc.decode(__encoding__)
        else:
            html = doc.decode(encoding)
        return html

    return wrapper


# 参数类型：QueryString
@safe
@auto_decode
def get(url, params=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    resp = __opener.open(url)
    return resp


# 提交RequestPayload
def postPayload(url, params):
    postData = json.dumps(params).encode()
    return __opener.open(url, postData).read().decode(encoding)


def addHeader(head_dict):
    if head_dict:
        # list
        header = []
        for key, value in head_dict.items():
            elem = (key, value)
            header.append(elem)
        # 自动在发出的 GET 或者 POST 请求中加上自定义的 Header
        # addheaders是list，元素是tuple
        __opener.addheaders.extend(header)


def parseJson(str):
    return json.loads(str)


def setAgent(
        value="Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"):
    for elem in __opener.addheaders:
        # elem是tuple，不可增删改
        if elem[0] == "User-agent":
            __opener.addheaders.remove(elem)
    __opener.addheaders.append(("User-agent", value))


setDefaultAgent = partial(setAgent,
                          value="Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
setMobileAgent = partial(setAgent, value="app-iphone-client-(null)-2F1582A1-E089-4446-A561-3D695610241C")
