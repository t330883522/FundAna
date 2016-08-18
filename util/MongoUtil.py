# @Author  : JL
# @Time    : 2016/7/30 23:25
import pymongo
#连接mongodb
from fund import FundUtil

client=pymongo.MongoClient("23.105.214.4", 27017)
#创建数据库
db=client["fund"];
coll=db.collection_names(False)
print(type(coll),len(coll))
funds=FundUtil.getFundsByDT(2000)
for f in funds:
    if f.code not in coll:
        print(f.code)


def insertInverst(fund):
    #创建表单
    sheet=db[fund.code]
    for key ,value  in fund.dalprc.items():
        obj={
            "date":key,
            "jz":value
            }
        #新增
        sheet.insert(obj)


