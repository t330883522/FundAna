import pymongo
#连接mongodb
client=pymongo.MongoClient("23.105.214.4", 27017)
#创建数据库
fund=client["fund"];
#创建表单
history=fund["history"];
obj={
    "code":"160119",
    "price":"1.02312"
}
#新增
history.insert(obj)
#查询
#小于或等于$lte
#大于或等于$lte
#$ne不等于
for item in history.find({'date':{"$lte":"20160101","$gte":"20150101"}}):
    print(item)