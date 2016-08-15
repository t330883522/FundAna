from datetime import datetime

import numpy
from dateutil.relativedelta import relativedelta

from ReqWorker import ReqWorker
from fund import FundUtil
from fund.FundUtil import Fund
from queue import Queue
from time import time
import os
import logging

from util import HttpUtil

funds = FundUtil.getFundsByDT(2000,page=1)
# funds=[Fund('001302')]
print("获取基金：%s"%len(funds))

ts = time()
queue = Queue()
# Create a queue to communicate with the worker threads
# Create 8 worker threads
# 创建八个工作线程
for x in range(200):
    worker = ReqWorker(queue)
    # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
    worker.daemon = True
    worker.start()
for fund in funds:
    # Put the tasks into the queue as a tuple
    # 将任务以tuple的形式放入队列中
    logging.info('Queueing {}'.format(fund.code))
    queue.put((fund))
    # Causes the main thread to wait for the queue to finish processing all the tasks
# 让主线程等待队列完成所有的任务
#如果线程在queue.task_done()之前异常退出，则一直join
#如果thread.join()如果线程异常退出，join()也执行完成
queue.join()
print('Took {}'.format(time() - ts))

funds=sorted(funds, reverse=True)
print("基金方差从大到小排序")
print("排序    代码       离异系数  定投收益     定投收益/天    起始价格段位   结束价格段位  当前价格段位      收益平均值      最大收益      金额      开始      结束")
for index,fund in enumerate(funds):
    if datetime.strptime("20160801","%Y%m%d").date() not in fund.dalprc.keys():
        continue
    start,end=fund.getPOC()
    # start=(datetime.now()- relativedelta(years=1)).date()
    # if sorted(tuple(fund.dalprc.keys()))[0]>start:
    #     start = sorted(tuple(fund.dalprc.keys()))[0]
    # end=datetime.now().date()
    # if sorted(tuple(fund.dalprc.keys()))[-1]<end:
    #     end = sorted(tuple(fund.dalprc.keys()))[-1]
    rates,inversted=FundUtil.radical_inverstment_no_up(fund,startdate=start,enddate=end)
    startprices=[]
    endprices=[]
    for key,value in fund.dalprc.items():
        if key<=start:
            startprices.append(value)
        if key<=end:
            endprices.append(value)
    try :
        pricevalues=list(fund.dalprc.values())
        ratevalues=list(rates.values())
        print("%s    %s   %s    %s    %s   %s   %s   %s    %s    %s   %s    %s   %s"%(index+1,fund.code,fund.std*10000,ratevalues[-1],100000*ratevalues[-1]/int((end-start).days),fund.dalprc[start]/numpy.mean(startprices),fund.dalprc[end]/numpy.mean(endprices),(fund.valuation/fund.mean),numpy.mean(tuple(rates.values())),sorted(rates.values(),reverse=True)[0],numpy.sum(list(inversted.values())),start,end))
    except Exception as error:
        #以ERROR级别记录日志消息，除了打印传入的msg，异常跟踪信息将被自动添加到日志消息里
        pass
        # logging.exception(fund.code)