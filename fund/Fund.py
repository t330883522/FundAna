import logging

import numpy
import collections

class Fund:
    def __init__(self,code):
        self.code=code
        self.name=""
        #日期和累计净值的dict
        self.__dalprc__=collections.OrderedDict()
        #标准差
        self.std=0
        #方差
        # self.var=0
        #平均值
        self.mean=0
        self.valuation = 0
        pass

    #实现该方法可以被sorted
    def __lt__(self, y):  # 实现<操作
        return self.std< y.std


    @property
    def dalprc(self):
        return self.__dalprc__
    @dalprc.setter
    def dalprc(self,value):
        if not isinstance(value, collections.OrderedDict):
            raise TypeError("argument must be collections.OrderedDict")
        self.__dalprc__=value
        # mods=[]
        # for index,value in enumerate(list(self.dalprc.values())):
        #     if index:
        #         before=list(self.dalprc.values())[index-1]
        #         fab=(value-before)/before
        #         #mods.append(numpy.fabs(fab)*10000)
        #         mods.append(fab)
        #     else:
        #         mods.append(0)
        self.mean=numpy.mean(tuple(self.dalprc.values()))
        self.std=numpy.std(tuple(self.dalprc.values()))/self.mean
        #self.var=numpy.var(tuple(self.dalprc.values()))/self.mean
    def reversed(self):
        self.dalprc=collections.OrderedDict(zip(self.dalprc.keys(), reversed(self.dalprc.values())))
    # 获取价格曲线交点
    def getPOC(self):
        if  self.dalprc:
            sortedPrc = sorted(self.dalprc.items(), key=lambda d: d[1])
            dates=[]
            current=sortedPrc.pop()
            while sortedPrc:
                next=sortedPrc.pop()
                if next:
                    if abs(current[1]-next[1])<0.2:
                        dates.append((min(current[0],next[0]),max(current[0],next[0])))
                    current=next
                else:
                    break
            sortedArray=sorted(dates, key=lambda d: abs(d[0]-d[1]),reverse=True)
            return sortedArray[0]
        else:
            print('%s请获取价格...'%self.code)
    def __str__(self):
        return self.code+","+self.name
class Topic:
    def __init__(self,topic,name,syl=None):
        self.topic=topic
        self.name=name
        self.syl=syl
        self.__funds__=[]
    @property
    def funds(self):
        if not self.__funds__:
            from fund import FundUtil
            self.__funds__=FundUtil.getFundsByTopic(self.topic)
        return self.__funds__