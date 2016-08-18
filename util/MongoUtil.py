# @Author  : JL
# @Time    : 2016/7/30 23:25
import pymongo
# 连接mongodb
from fund import FundUtil

client = pymongo.MongoClient("23.105.214.4", 27017)
# 创建数据库
db = client["fund"]
pool = db["pool"]
result = pool.create_index([('code', pymongo.ASCENDING)], unique=True)


# 打印主键信息
# print(pool.index_information())


def insertInverst(fund):
    # 创建表单
    sheet = db[fund.code]
    for key, value in fund.dalprc.items():
        obj = {
            "date": key,
            "jz": value
        }
        # 新增
        sheet.insert(obj)
