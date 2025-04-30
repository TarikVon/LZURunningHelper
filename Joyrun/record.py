#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: Joyrun/record.py
#
# 跑步记录类
#

import os
import time
import uuid
import math
from functools import partial

try:
    from ..util import (
        json_load,
        json, random,
    )
except (ImportError, SystemError, ValueError):
    import sys

    sys.path.append('../')
    from util import (
        json_load,
        json, random,
    )

Work_Dir = os.path.join(os.path.dirname(__file__))  # 当前工作路径
Data_Dir = os.path.join(Work_Dir, "data/")

json_load = partial(json_load, Data_Dir)

__Record_Base__ = ["Record", "RecordDongCao", "RecordXiCao", ]  # 基类
__Record_XiCao_Instance__ = ["RecordXiCao_1", ]  # 未名湖跑步记录实例
__Record_DongCao_Instance__ = ["RecordDongCao_1", ]

__all__ = __Record_Base__ + __Record_XiCao_Instance__ + __Record_DongCao_Instance__


class Record(object):
    """ 跑步记录 基类

        Attributes:
            class:
                A_Loop_GPS_JSON    str      一套 GPS 数据
                A_Loop_Distance    float    一套 GPS 数据对应的距离/km
                Altitude_Max       float    最高海拔
                Altitude_Min       float    最低海拔
            instance:
                altitude           list     海拔数据点
                dateline           int      上传时间？？
                starttime          int      开始时间/s
                content            list     路径 GPS 数据点 -> [latitude, longitude]
                second             int      跑步时长/s
                stepcontent        list     每个采样点的步速 -> [step_num, second] -> avg spped
                stepremark         list     意义未知！！！
                runid              str      跑步记录数据库 id
                sampleinterval     int      采样点时间间隔/s
                meter              int      跑步距离/m
                totalsteps         int      总步数
                nodetime           list     节点信息 -> [meter, second, latitude, longitude, points_num]
                lasttime           int      结束时间/s
                timeDistance       list     各个采样点对应的跑步距离

                distance           float    预设跑步距离/km
                pace               float    预设跑步速度/(min/km)
                stride_frequncy    int      预设步频/(step/min)
    """
    A_Loop_GPS_JSON = ""
    A_Loop_Distance = 0.00

    Altitude_Max = 0.00
    Altitude_Min = 0.00

    def __init__(self, distance, pace, stride_frequncy):
        """ 由距离、速度、步频来生成一次跑步记录

            Args:
                distance           float   跑步距离/km
                pace               float   跑步速度/(min/km)
                stride_frequncy    int     步频/(step/min)
        """
        if self.__class__.__name__ in __Record_Base__:  # 基类不可实例化
            raise NotImplementedError

        self.altitude = []
        self.dateline = 0
        self.starttime = 0
        self.content = []
        self.second = 0
        self.stepcontent = []
        self.stepremark = []  # 意义未知，因此默认为空
        self.runid = ""
        self.sampleinterval = 5  # 默认为 5s ，从 apk 反编译结果来看，时间超过 6h 会变成 10s ，同时采样量减半
        self.meter = 0
        self.totalsteps = 0
        self.nodetime = []
        self.lasttime = 0
        self.timeDistance = []

        self.distance = distance
        self.pace = pace
        self.stride_frequncy = stride_frequncy

        self.__build()
        self.__format()

    def __get_runid(self):
        """ 生成 runid

            从 apk 反编译结果来看，好像是通过 随机 uuid 生成的 32 位随机串
        """
        return uuid.uuid4().hex  # uuid4 -> Generate a random UUID.

    def __upload_delay(self):
        """ 生成 上传记录 与 结束跑步 之间的时间间隔
        """
        return random.randint(10, 20)  # 10~20s 的间隔

    def __stride_frequncy_delta(self):
        """ 步频随机偏移量
        """
        return int((random.random() - 0.5) * 2 * 15)  # 15 step/min

    def __distance_delta(self):
        """ 距离随机偏移量
        """
        return (random.random() - 0.5) * 2 * self.distance * 0.05  # 预设距离上下浮动 5%

    def __altitude_delta(self):
        """ 海拔随机偏移量
        """
        return random.random() * (self.Altitude_Max - self.Altitude_Min) * 0.1  # 每次最大浮动极差的 10%

    def __point_delta(self):
        """ 坐标随机偏移量
        """
        return int((random.random() - 0.5) * 2 * 0.000025 * 1000000)  # 0.000025

    def __stepcontent_repeat(self):
        """ 步速采样点点重复次数
        """
        return random.choices([1, 2, 3, 4, 5], weights=[5, 4, 3, 2, 1], k=1)[0]  # 重复 1-5 次，次数越大概率越低

    def __get_stepcontent_point(self):
        """ 生成一个步速采样点

            由步数生成时间
        """
        step_count = random.randint(9, 12)  # 一次 9 - 12 步
        step_time = step_count / self.stride_frequncy * 60
        step_time *= (1.0 + (random.random() - 0.5) * 2 * 0.05)  # 引入 5% 的速率浮动
        return [step_count, round(step_time, 2)]  # 时间取 2 位小数

    def __get_meter_increment(self):
        """ 生成一个距离增量

            参考： 如果配速 5.50 min/km ，则 5s 跑 15.2 m ，则上下浮动 2m 相当于 上下浮动 13.2 %
        """
        meter_increment = 1000 / self.pace / 60 * self.sampleinterval
        meter_increment *= (1.0 + (random.random() - 0.5) * 2 * 0.07)  # 上下浮动 7%
        return int(meter_increment)

    def __node_second_delta(self):
        """ 生成节点秒数随机偏移量
        """
        return random.randint(-10, 10)  # 上下浮动 10s

    def __altitude_generator(self):
        """ 随机海拔 生成器

            通过模拟随机漫步
        """
        current_altitude = (self.Altitude_Max + self.Altitude_Min) / 2
        while True:
            delta = self.__altitude_delta()
            if current_altitude + delta > self.Altitude_Max:
                current_altitude -= delta
            elif current_altitude - delta < self.Altitude_Min:
                current_altitude += delta
            else:
                current_altitude += random.randrange(-1, 2, 2) * delta  # random.randrange(-1,2,2) 生成符号位
            yield round(current_altitude, 2)  # 2 位小数

    def __point_generator(self):
        """ GPS 坐标 生成器

            无限循环跑圈，并对每个点都引入一个偏差量
        """
        points_per_loop = json_load(self.A_Loop_GPS_JSON)
        points_num_per_loop = int(self.pace * self.A_Loop_Distance * 60 / self.sampleinterval)
        while True:
            for i in range(points_num_per_loop):
                idx = math.floor(i / points_num_per_loop * len(points_per_loop))
                point = points_per_loop[idx].copy()  # 一定要 copy 否则会同步修改
                point[0] += self.__point_delta()
                point[1] += self.__point_delta()
                yield point

    def __stepcontent_generator(self):
        """ 步速 生成器

            离散点 (步数, 时间) -> 步速 (step/min)
            每个离散点会重复几次
        """
        total_repeat = self.__stepcontent_repeat()
        current_repeat = 0
        step_point = self.__get_stepcontent_point()
        while True:
            yield step_point
            current_repeat += 1
            if current_repeat >= total_repeat:  # 重新初始化重复次数
                total_repeat = self.__stepcontent_repeat()
                current_repeat = 0
                step_point = self.__get_stepcontent_point()

    def __timeDistance_generator(self):
        """ 距离对时间离散点 生成器

            描述每个采样点对应的跑步距离
        """
        current_meter = 0
        while True:
            current_meter += self.__get_meter_increment()
            yield current_meter

    def __build(self):
        """ 构造记录

            共需构造 13 个量
            需要同步构造 altitude, content, stepcontent, timeDistance 四个列表
                    和 stepremark, nodetime

            目前 stepcontent 的意义尚不明确，就默认为空了
        """
        self.runid = self.__get_runid()
        self.dateline = int(time.time())  # 上传时间
        self.lasttime = self.dateline - self.__upload_delay()

        self.second = int((self.distance + self.__distance_delta()) * self.pace * 60)
        self.starttime = self.lasttime - self.second

        """ 接下来构造 6 个离散点序列 """

        altitude_gen = self.__altitude_generator()
        point_gen = self.__point_generator()
        stepcontent_gen = self.__stepcontent_generator()
        timeDistance_gen = self.__timeDistance_generator()

        total_points_num = math.ceil(self.second / self.sampleinterval)  # 以 sampleinterval 决定采样点总数，包含最后一个不足 interval 的点
        current_point_num = 0

        node_meter = 1000  # 节点距离
        node_second = 0  # 节点秒数

        while current_point_num < total_points_num:
            self.altitude.append(next(altitude_gen))
            self.content.append(next(point_gen))
            self.stepcontent.append(next(stepcontent_gen))
            self.timeDistance.append(next(timeDistance_gen))

            if self.timeDistance[-1] >= node_meter:
                node_second = math.floor(self.second * node_meter / self.distance / 1000)
                node_second_delta = self.__node_second_delta()
                if node_second + node_second_delta >= self.second:  # 确保不超过最大秒数
                    pass  # 如果已经贴近最大秒数，则不做浮动
                else:
                    node_second += random.randrange(-1, 2, 2) * node_second_delta  # 否则上下随机浮动 delta
                self.nodetime.append([
                    node_meter,  # 节点距离/m
                    node_second,  # 到达该节点的时间
                    self.content[-1][0],  # 纬度
                    self.content[-1][1],  # 经度
                    len([d for d in self.timeDistance if d <= node_meter]),  # 该节点前的采样点数量
                ])
                node_meter += 1000

            current_point_num += 1

        self.meter = self.timeDistance[-1]  # 最后一个采样点的距离对应于总距离
        self.totalsteps = sum(x[0] for x in self.stepcontent)  # 所有 stepcontent 中的步数之和

    def __format(self):
        """ 将 list 字段格式化成 json 字符串
        """
        json_dumps = partial(json.dumps, separators=(',', ':'))  # 自定义 json.dumps 函数 确保分隔符间没有空格

        if self.nodetime == []:  # 如果没有 node 则为 ""
            self.nodetime = ""
        else:
            self.nodetime = "-".join([json_dumps(node) for node in self.nodetime])

        if self.stepremark == []:  # 没有搞懂这个参数的意思，所以暂且默认为空啦～ 好像是表示异常步数记录点
            self.stepremark = ""
        else:
            raise NotImplementedError

        self.altitude = json_dumps(self.altitude)
        self.content = "-".join([json_dumps(point) for point in self.content])
        self.stepcontent = json_dumps(self.stepcontent)
        self.timeDistance = json_dumps(self.timeDistance)


class DongCao(Record):
    """ 东操跑步记录 基类
    """
    pass


class XiCao(Record):
    """ 西操跑步记录 基类
    """
    pass


class RecordXiCao_1(XiCao):
    """ 西操跑步记录 No.1
    """

    A_Loop_GPS_JSON = "xicao.joyrun.json"
    A_Loop_Distance = 0.4

    Altitude_Max = 1745.00
    Altitude_Min = 1743.00


class RecordDongCao_1(DongCao):
    """ 东操跑步记录 No.1
    """

    A_Loop_GPS_JSON = "dongcao.joyrun.json"
    A_Loop_Distance = 0.4

    Altitude_Max = 1745.00
    Altitude_Min = 1743.00
