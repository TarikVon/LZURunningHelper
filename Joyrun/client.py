#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: Joyrun/client.py
#
# Joyrun 客户端类
#

import os
import time
from functools import partial, wraps
import requests
from urllib.parse import quote

try:
    from . import record
    from .auth import JoyrunAuth
    from .error import (
        JoyrunRequestStatusError,
        JoyrunRetStateError,
        JoyrunSidInvalidError,
    )
except (ImportError, SystemError, ValueError):
    import record
    from auth import JoyrunAuth
    from error import (
        JoyrunRequestStatusError,
        JoyrunRetStateError,
        JoyrunSidInvalidError,
    )

try:
    from ..util import (
        Config,
        Logger,
        pretty_json,
        json_load,
        json_dump,
        MD5,
        json,
        JSONDecodeError,
        random,
        RecordTypeError,
        RecordNumberError,
    )
except (ImportError, SystemError, ValueError):
    import sys

    sys.path.append("../")
    from util import (
        Config,
        Logger,
        pretty_json,
        json_load,
        json_dump,
        MD5,
        json,
        JSONDecodeError,
        random,
        RecordTypeError,
        RecordNumberError,
    )


Root_Dir = os.path.join(os.path.dirname(__file__), "../")
Cache_Dir = os.path.join(Root_Dir, "cache/")

json_load = partial(json_load, Cache_Dir)
json_dump = partial(json_dump, Cache_Dir)

config = Config()


__all__ = [
    "JoyrunClient",
]


def sid_invalid_retry(retry=1):
    """会话 ID 失效，一般是因为在手机上登录，导致上次登录的 sid 失效。
    该函数用于返回一个函数修饰器，被修饰的 API 函数如果抛出 sid 失效错误，
    则重新登录后重新调用 API 函数，最高 retry 次

    Args:
        retry    int    重新尝试的次数，默认只重试一次
    Raises:
        JoyrunSidInvalidError    超过重复校验次数后仍然鉴权失败
    """

    def func_wrapper(func):
        @wraps(func)
        def return_wrapper(self, *args, **kwargs):
            count = 0
            while True:
                try:
                    return func(self, *args, **kwargs)
                except JoyrunSidInvalidError:  # 该错误类捕获 鉴权失败 的异常
                    count += 1
                    if count > retry:
                        break
                    else:
                        self.logger.debug("sid invalid, retry %s" % count)
                        self.login()
                except Exception as err:
                    raise err
            raise JoyrunSidInvalidError("reach retry limit %s" % retry)

        return return_wrapper

    return func_wrapper


class JoyrunClient(object):
    """Joyrun 悦跑圈客户端类

    Attributes:
        class:
            logger                Logger            日志类实例
            BaseUrl               str               API 基础链接
            Cache_LoginInfo       str               登录状态缓存 json 文件名
        instance:
            userName              str               登录用户名
            password              str               登录密码
            session               request.Session   requests 会话类实例
            auth                  JoyrunAuth        Jourun 请求鉴权类实例
            uid                   int               用户 ID
            sid                   str               会话 ID
            base_headers          dict              基础请求头
            device_info_headers   dict              设备信息请求头
    """

    logger = Logger("joyrun")
    BaseUrl = "https://api.thejoyrun.com"
    Cache_LoginInfo = "Joyrun_LoginInfo.json"

    def __init__(self):
        self.userName = "{studentId}{suffix}".format(studentId=config.get("Joyrun", "StudentID"), suffix=config.get("Joyrun", "suffix"))
        self.password = config.get("Joyrun", "Password")

        try:
            cache = json_load(self.Cache_LoginInfo)
        except (FileNotFoundError, JSONDecodeError):
            cache = {}

        if cache.get("userName") == self.userName:
            self.uid = cache.get("uid", 0)
            self.sid = cache.get("sid", "")
        else:  # userName 不匹配，则不使用缓存信息
            self.uid = 0
            self.sid = ""

        self.session = requests.Session()

        self.session.headers.update(self.base_headers)
        self.session.headers.update(self.device_info_headers)

        self.auth = JoyrunAuth(self.uid, self.sid)

        if self.uid and self.sid:  # 直接从缓存中读取登录状态
            self.__update_loginInfo()
        else:
            self.login()  # 否则重新登录

    @property
    def base_headers(self):
        return {
            "Accept-Language": "en_US",
            "User-Agent": "okhttp/3.10.0",
            "Host": "api.thejoyrun.com",
            "Connection": "Keep-Alive",
        }

    @property
    def device_info_headers(self):
        return {
            "MODELTYPE": "Xiaomi MI 5",
            "SYSVERSION": "8.0.0",
            "APPVERSION": "4.2.0",
            "MODELIMEI": "861945034544449",
            "APP_DEV_INFO": "Android#4.2.0#Xiaomi MI 5#8.0.0#861945034544449#%s#xiaomi" % (self.uid or 87808183),
        }

    def __reqeust(self, method, url, **kwargs):
        """网路请求函数模板，对返回结果做统一校验

        Args:
            method            str    请求 method
            url               str    请求 url/path
            **kwargs                 传给 requests.request 函数
        Returns:
            respJson      jsonData   json 数据
        Raises:
            JoyrunRequestStatusError    请求状态码异常
            JoyrunRetStateError         ret 字段非 0 -> 请求结果异常
            JoyrunSidInvalidError       sid 失效，登录状态异常
        """
        if url[:7] != "http://" and url[:8] != "https://":
            url = "{base}/{path}".format(base=self.BaseUrl, path=url[1:] if url[0] == "/" else url)  # //user/login/normal 需要保留两个 '/' !

        resp = self.session.request(method, url, **kwargs)
        # self.logger.debug("request.url = %s" % resp.url)
        # self.logger.debug("request.headers = %s" % resp.request.headers)
        # self.logger.debug("request.body = %s" % resp.request.body)
        # self.logger.debug("response.headers = %s" % resp.headers)

        if not resp.ok:
            self.logger.error("request.url = %s" % resp.url)
            self.logger.error("request.headers = %s" % pretty_json(dict(resp.request.headers)))
            self.logger.error("session.cookies = %s" % pretty_json(self.session.cookies.get_dict()))
            if resp.request.method == "POST":
                self.logger.error("request.body = %s" % resp.request.body)
            self.logger.error("response.text = %s" % resp.text)
            raise JoyrunRequestStatusError("response.ok error")

        respJson = resp.json()
        if respJson.get("ret") != "0":
            if respJson.get("ret") == "401":  # sid 失效
                raise JoyrunSidInvalidError("sid invalid")
            else:
                self.logger.error("response.json = %s" % pretty_json(respJson))
                raise JoyrunRetStateError("response.json error")

        self.logger.debug("request.url = %s" % resp.url)
        self.logger.debug("response.json = %s" % pretty_json(respJson))

        return respJson

    def get(self, url, params={}, **kwargs):
        return self.__reqeust("GET", url, params=params, **kwargs)

    def post(self, url, data={}, **kwargs):
        return self.__reqeust("POST", url, data=data, **kwargs)

    def __update_loginInfo(self):
        """更新登录状态信息

        更新本地 uid, sid 记录
        更新鉴权实例 uid, sid 记录
        更新 cookies 信息
        更新 headers 设备信息
        """
        self.auth.reload(uid=self.uid, sid=self.sid)
        loginCookie = "sid=%s&uid=%s" % (self.sid, self.uid)
        self.session.headers.update({"ypcookie": loginCookie})
        self.session.cookies.clear()
        self.session.cookies.set("ypcookie", quote(loginCookie).lower())
        self.session.headers.update(self.device_info_headers)  # 更新设备信息中的 uid 字段

    def __parse_record(self, respJson):
        """解析 get_record 返回的 json 包"""
        r = respJson["runrecord"]
        r["altitude"] = json.loads(r["altitude"])
        r["heartrate"] = json.loads(r["heartrate"])
        r["stepcontent"] = [[json.loads(y) for y in x] for x in json.loads(r["stepcontent"])]
        r["stepremark"] = json.loads(r["stepremark"])
        r["content"] = [json.loads(x) for x in r["content"].split("-")]
        return respJson

    def get_timestamp(self):
        respJson = self.get("/GetTimestamp.aspx")

    @sid_invalid_retry(1)
    def get_dataMessages(self):
        params = {
            "lasttime": 0,
        }
        respJson = self.get("/dataMessages", params, auth=self.auth.reload(params))

    def login(self):
        """登录 API"""
        params = {
            "username": self.userName,
            "pwd": MD5(self.password).upper(),
        }
        respJson = self.get("//user/login/normal", params, auth=self.auth.reload(params))

        self.sid = respJson["data"]["sid"]
        self.uid = int(respJson["data"]["user"]["uid"])

        json_dump(self.Cache_LoginInfo, {"userName": self.userName, "sid": self.sid, "uid": self.uid})  # 缓存新的登录信息
        self.__update_loginInfo()

    def logout(self):
        """登出 API
        登出后 sid 仍然不会失效 ！ 可能是闹着玩的 API ...
        """
        respJson = self.post("/logout.aspx", auth=self.auth.reload())

    @sid_invalid_retry(1)
    def get_bindings(self):
        respJson = self.get("//user/getbindings", auth=self.auth.reload())

    @sid_invalid_retry(1)
    def get_myInfo(self):
        """获取用户信息 API"""
        payload = {
            "touid": self.uid,
            "option": "info",
        }
        respJson = self.post("/user.aspx", payload, auth=self.auth.reload(payload))

    @sid_invalid_retry(1)
    def get_myInfo_detail(self):
        payload = {
            "option": "get",
        }
        respJson = self.post("/oneclickdetails.aspx", payload, auth=self.auth.reload(payload))

    @sid_invalid_retry(1)
    def get_friends(self):
        payload = {"dateline": 1, "option": "friends"}
        respJson = self.post("/user.aspx", payload, auth=self.auth.reload(payload))

    @sid_invalid_retry(1)
    def get_feed_messages(self):
        payload = {
            "lasttime": 0,
        }
        respJson = self.post("/feedMessageList.aspx", payload, auth=self.auth.reload(payload))

    @sid_invalid_retry(1)
    def get_feed_remind(self):
        respJson = self.post("/Social/GetFeedRemind.aspx", auth=self.auth.reload())

    @sid_invalid_retry(1)
    def get_records(self):
        """获取跑步记录 API"""
        payload = {
            "year": 0,
        }
        respJson = self.post("/userRunList.aspx", payload, auth=self.auth.reload(payload))

    @sid_invalid_retry(1)
    def get_best_record(self):
        payload = {
            "touid": self.uid,
            "option": "record",
        }
        respJson = self.post("/run/best", payload, auth=self.auth.reload(payload))

    @sid_invalid_retry(1)
    def get_record(self, fid):
        """获取跑步单次记录详情 API"""
        payload = {
            "fid": fid,
            "wgs": 1,
        }
        respJson = self.post("/Run/GetInfo.aspx", payload, auth=self.auth.reload(payload))
        json_dump("record.%s.json" % fid, respJson)
        json_dump("record.%s.parse.json" % fid, self.__parse_record(respJson))

    @sid_invalid_retry(1)
    def upload_record(self, record):
        """上传跑步记录"""
        payload = {
            "altitude": record.altitude,
            "private": 0,
            "dateline": record.dateline,
            "city": "兰州",
            "starttime": record.starttime,
            "type": 1,
            "content": record.content,
            "second": record.second,
            "stepcontent": record.stepcontent,
            "province": "甘肃省",
            "stepremark": record.stepremark,
            "runid": record.runid,
            "sampleinterval": record.sampleinterval,
            "wgs": 1,
            "nomoment": 1,
            "meter": record.meter,
            "heartrate": "[]",
            "totalsteps": record.totalsteps,
            "nodetime": record.nodetime,
            "lasttime": record.lasttime,
            "pausetime": "",
            "timeDistance": record.timeDistance,
        }
        # self.logger.info(pretty_json(payload))
        respJson = self.post("/po.aspx", payload, auth=self.auth.reload(payload))

    def run(self):
        """项目主程序外部调用接口"""
        distance = config.getfloat("Joyrun", "distance")  # 总距离 km
        pace = config.getfloat("Joyrun", "pace")  # 速度 min/km
        stride_frequncy = config.getint("Joyrun", "stride_frequncy")  # 步频 step/min
        record_type = config.get("Joyrun", "record_type")  # 跑步记录类型
        record_number = config.getint("Joyrun", "record_number")  # 跑步记录编号

        if record_type == "xicao":
            record_instances = record.__Record_XiCao_Instance__
        elif record_type == "dongcao":
            record_instances = record.__Record_DongCao_Instance__
        elif record_type == "random":
            record_instances = getattr(record, random.choice(["__Record_XiCao_Instance__", "__Record_DongCao_Instance__"]))
        else:
            raise RecordTypeError("unsupport record type '%s' ! valid type = ['xicao','dongcao','random']" % record_type)

        if record_number == 0:
            Record = getattr(record, random.choice(record_instances))
        elif record_number < 0 or record_number > len(record_instances):
            raise RecordNumberError("invalid record number '%s' ! valid range = [0,%s]" % (record_number, len(record_instances)))
        else:
            Record = getattr(record, record_instances[record_number - 1])

        _record = Record(distance, pace, stride_frequncy)
        self.upload_record(_record)


if __name__ == "__main__":
    client = JoyrunClient()
    # client.run()

    # client.get_timestamp()
    # client.get_dataMessages()
    # client.login()
    # client.logout()
    # client.get_myInfo()
    # client.get_myInfo_detail()
    # client.get_feed_messages()
    # client.get_feed_remind()
    # client.get_friends()
    # client.get_bindings()
    # client.get_records()
    # client.get_best_record()
    # client.get_record(249654660)
