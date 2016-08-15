import datetime

import matplotlib.pyplot as plt
import numpy
from matplotlib.dates import *

from fund import FundUtil
from fund.Fund import Fund
from pylab import *

#缺省情况下，matplotlib是无法显示中文的，主要原因是没有指定中文字体（文件）
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
class FundPlot:
    def __init__(self):
        self.__fig, self.__ax = plt.subplots()


    def setPlot(self, dates, y):
        self.__ax.plot_date(dates, y, 'm-', marker='.',color="red", linewidth=2)
        # 设置X轴范围，可以取任意时间，不根据X坐标来
        #self.__ax.set_xlim(dates[0], datetime.datetime.strptime("2016-08-01", "%Y-%m-%d"))
        # 设置时间间隔：(byweekday=1, interval=1)
        # byweekday=0表示星期一
        # interval=1表示每1个星期一是刻度
        self.__ax.xaxis.set_major_locator(WeekdayLocator(0, 4))
        # 设置X轴的时间格式
        # 完整的：%Y-%m-%d %H:%M:%S
        self.__ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        # 设置横坐标的时间格式
        self.__ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
        # 设置x轴时间外观
        self.__fig.autofmt_xdate()


plot1 = FundPlot()
plot2 = FundPlot()
fund = Fund("162411")
results = FundUtil.prices(fund.code)

fund.dalprc = results
#fund.reversed()
rates, inversts = FundUtil.radical_inverstment_no_up(fund,startdate="2015-10-9",enddate="2016/8/11",down_pow=80)
#fund.dalprc.values()如果不list，长度只有1
start=list(rates.keys())[0]
end=list(rates.keys())[-1]
plt.title(u"%s至%s 定投%s-%s收益率"%(start,end,fund.code,fund.name))
for key ,value in rates.items():
    if value==sorted(rates.values(),reverse=True)[0]:
        annotate(value,xy=(key,value))
    endx=key
    endy=value
annotate(endy,xy=(endx,endy))
plot2.setPlot([k for k in fund.dalprc.keys()], list(fund.dalprc.values()))
plot2.setPlot([k for k in rates.keys()], list(rates.values()))
#plot2.show()
plt.title(u"%s至%s 定投%s-%s总投资%s"%(start,end,fund.code,fund.name,numpy.sum(tuple(inversts.values()))))
plot1.setPlot([k for k in inversts.keys()], list(inversts.values()))
plt.show()
