# @Author  : JL
# @Time    : 2016/8/15 0:28
from datetime import datetime

from util import MongoUtil


class FundInv:
    def __init__(self, code, minInv, startMoney=0, startShare=0):
        self.code = code
        self.minInv = minInv
        self.startMoney = startMoney
        self.startShare = startShare
        self._history = []

    def insert(self):
        print(self.__dict__)
        MongoUtil.pool.delete_one({"code":self.code});
        MongoUtil.pool.insert(self.__dict__);
        print(MongoUtil.db.collection_names(include_system_collections=False))

    @property
    def history(self):
        self._history = MongoUtil.pool.find()
        return self._history

    @history.setter
    def history(self, value):
        self._history = value


class Inverst:
    def __init__(self, date, money, gz, kpow):
        self.date = date
        self.gz = gz
        self.money = money


fi = FundInv("162411", 100, startMoney=100, startShare=169.81)
fi.insert()
inv=Inverst(datetime.now().date(),150,0.8,50)
print(inv.__dict__)
MongoUtil.pool.update({"code":"162411"},{"$push":  {"_history":inv.__dict__}})