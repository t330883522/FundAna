import datetime
from dateutil.relativedelta import relativedelta
import collections
import logging

import numpy
from bs4 import BeautifulSoup

import re

from fund.Fund import Fund, Topic
from util import HttpUtil
from functools import partial
from rolex import rolex
# 获取默认长度为100条的定投排行
def getFundsByDT(size=100,page=1):
    HttpUtil.setMobileAgent()
    url_funds = "http://fundex2.eastmoney.com/FundMobileApi/FundInvestmentRankList.ashx"
    params = {
        "FundType": "0",
        "SortColumn": "DT_1N",
        "Sort": "desc",
        "pageIndex": page,
        "pageSize": size,
        "BUY": "true",
        "CompanyId": "",
        "deviceid": "8561658B-9306-4642-A86D-6CAFD29E9C90",
        "plat": "iPhone",
        "product": "EFund",
        "version": "4.2.3"
    }
    response = HttpUtil.get(url_funds, params);
    obj = HttpUtil.parseJson(response)
    funds = []
    for fund in obj["Datas"]:
        funds.append(Fund(fund["FCODE"]))
        funds[-1].name = fund["SHORTNAME"]
    HttpUtil.setDefaultAgent()
    return funds

# getQDII=pa

# 获取默认长度为100条的基金排行
#0:全部；6:QDII
def getFundsByType(size=100,type=0,page=1):
    HttpUtil.setMobileAgent("app-iphone-client-(null)-2F1582A1-E089-4446-A561-3D695610241C")
    url_funds = "http://fundex2.eastmoney.com/FundMobileApi/FundRankNewList.ashx"
    params = {
        "FundType": type,
        "SortColumn": "RZDF",
        "Sort": "desc",
        "pageIndex": page,
        "pageSize": size,
        "BUY": "true",
        "CompanyId": "",
        "deviceid": "8561658B-9306-4642-A86D-6CAFD29E9C90",
        "plat": "iPhone",
        "product": "EFund",
        "version": "4.2.3"
    }
    response = HttpUtil.get(url_funds, params);
    obj = HttpUtil.parseJson(response)
    funds = []
    for fund in obj["Datas"]:
        funds.append(Fund(fund["FCODE"]))
        funds[-1].name = fund["SHORTNAME"]
    HttpUtil.setDefaultAgent()
    return funds
def getFundsByTopic(tp):
    pattern=re.compile(r'[a-z0-9]{16}')
    if not pattern.match(tp):
        for topic in topics():
            if topic[1]==tp:
                tp=topic[0]
                break
    url='http://fund.eastmoney.com/api/FundTopicInterface.ashx'
    params={
        'callbackname' : 'topicFundData' ,
        'sort' : 'SYL_6Y',
        'sorttype' : 'DESC' ,
        'pageindex' : 1 ,
        'pagesize' : 10 ,
        'dt' : 10 ,
        'tp' : tp
    }
    json=HttpUtil.get(url,params)
    pattern = re.compile(r'\{.*\}')
    # 返回集合
    matches = pattern.findall(json)
    funds=[]
    if matches:
        obj=HttpUtil.parseJson(matches[0])
        for item in obj["Datas"]:
            fund=Fund(item["FCODE"])
            fund.name=item["SHORTNAME"]
            funds.append(fund)
    else:
        logging.error("%s返回异常"%url)
    return funds

def valuation(code):
    # 估算的url
    url_valuation = "http://fundex2.eastmoney.com/FundMobileApi/FundVarietieValuationDetail.ashx"
    params = {
        "FCODE": code,
        "deviceid": "8561658B-9306-4642-A86D-6CAFD29E9C90",
        "plat": "iPhone",
        "product": "EFund",
        "version": "4.2.3"
    }
    response = HttpUtil.get(url_valuation, params);
    obj = HttpUtil.parseJson(response)
    try:
        gz = float(obj["Expansion"]["GZ"])
    except:
        gz = 1000
    time = obj["Expansion"]["GZTIME"]
    zd = obj["Expansion"]["GSZZL"]
    # 时间，估值，涨跌
    return (time, gz, zd)

def topics():
    url='http://fund.eastmoney.com/api/FundTopicInterface.ashx'
    params={
        "callbackname" :"fundData",
        "sort" : "SYL_Z",
        'sorttype' : 'desc',
        'pageindex' : 1 ,
        'pagesize' : 500 ,
        'dt' : 11 ,
        'tt' : 0 ,
        'rs' : 'WRANK'
    }
    json=HttpUtil.get(url,params)
    pattern = re.compile(r'\{.*?\}')
    # 返回集合
    matches = pattern.findall(json)
    topics=[]
    if matches:
        obj=HttpUtil.parseJson(matches[0])
        for item in obj["Datas"]:
            topics.append(item.split(","))
        return topics
    else:
        logging.error("%s返回异常"%url)

def prices(code ,startdate=(datetime.datetime.now() - relativedelta(years=2)).strftime("%Y%m%d"),
           enddate=datetime.datetime.now().strftime("%Y%m%d")):
    url = "http://finance.sina.com.cn/fund/api/xh5Fund/nav/%s.js" % code
    resp = HttpUtil.get(url)
    # 将正则表达式编译成Pattern对象
    #查找形似{...}的内容
    pattern = re.compile(r'\{.*?\}')
    # 返回集合
    matches = pattern.findall(resp)
    results = collections.OrderedDict()
    if matches:
        # 使用Match获得分组信息
        obj = HttpUtil.parseJson(matches[0]);
        data = obj["data"]
        datas = data.split("#")
        for tmp in datas:
            values = tmp.split(",")
            if startdate <= values[0] <= enddate:
                results[datetime.datetime.strptime(values[0], '%Y%m%d').date()] = float(values[2])
            # print("时间：%s 净值：%s 累计净值:%s "%(values[0],values[1],values[2]))
        results = collections.OrderedDict(reversed(list(results.items())))
        return results

def persistValues(code):
    url="http://finance.sina.com.cn/fund/api/xh5Fund/nav/%s.js"%code
    resp=HttpUtil.get(url)
    import re
    # 将正则表达式编译成Pattern对象
    pattern = re.compile(r'\{.*?\}')
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    ress = pattern.findall(resp)
    results = collections.OrderedDict()
    if ress:
        # 使用Match获得分组信息
        obj = HttpUtil.parseJson(ress[0]);
        data=obj["data"]
        datas=data.split("#")
        for tmp in datas:
            values=tmp.split(",")
            results[datetime.datetime.strptime(values[0],'%Y%m%d')]= float(values[1])
            #print("时间：%s 净值：%s 累计净值:%s "%(values[0],values[1],values[2]))
        results = collections.OrderedDict(reversed(list(results.items())))
        return results
# def save(fund):
#     for item in

def inverstment(fund, startdate=None,enddate=None,weekday=[0,1,2,3,4,5,6], base=100,up_pow=0,down_pow=0,no_up=False):
    # 总投资数额
    inversted = 0
    # 总份额
    amount = 0
    if not startdate:
        startdate=tuple(fund.dalprc.keys())[0]
    elif isinstance(startdate,str):
        startdate=rolex.str2date(startdate)
    if not enddate:
        enddate=tuple(fund.dalprc.keys())[-1]
    elif isinstance(enddate,str):
        enddate=rolex.str2date(enddate)
    # 每次投资的利率
    rates = collections.OrderedDict()
    # 每次投资的金额
    inversts = collections.OrderedDict()
    pre=None
    for date, price in fund.dalprc.items():
        if date>enddate or date<startdate:
            continue
        if date.weekday() in weekday:
            if not price:
                continue
            #平均成本价/当日价
            k = 1
            # if inversted > 0:
            #     k = (inversted / amount) / price
            # else:
            #     k = 1
            if pre :
                k = pre / price
            else:
                k = 1
            # 当天价格比成本价贵，少买
            if k < 1:
                if no_up:
                    money=0
                else:
                    money = base * pow(k, up_pow)
            else:
                 money=base*pow(k,down_pow)

            inversted += money
            inversts[date] = money
            amount += money / price
            zd = amount * price - inversted
            rates[date] = zd / inversted
            pre =price
    return rates, inversts
fool_inverstment=partial(inverstment)
radical_inverstment=partial(inverstment,up_pow=20,down_pow=20)
radical_inverstment_no_up=partial(radical_inverstment,no_up=True)
if __name__ == "__main__":
    for topic in topics():
        for fund in Topic(topic[0],topic[1]).funds:
            print(topic[1], end=',')
            print(fund)
    # fund=Fund("162411")
    # fund.dalprc = prices(fund.code)
    # fund.getPOC()
    # print(fool_inverstment(fund,startdate="20160726"))
    # print(radical_inverstment(fund,startdate="20160726"))
    # print(radical_inverstment_no_up(fund,startdate="20160726",down_pow=100))