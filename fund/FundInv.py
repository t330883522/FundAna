# @Author  : JL
# @Time    : 2016/8/15 0:28
from util import MongoUtil


class FundInv:
    pool = MongoUtil.db["pool"]

    def __init__(self, code, minInv, startMoney=0, startShare=0):
        self.code = code
        self.minInv = minInv
        self.startMoney = startMoney
        self.startShare = startShare
        self.__history__ = []

    def insert(self):
        global pool
        pool.insert(self);

    @property
    def history(self):
        global pool
        self.__history__ = pool.find()
        return self.__history__


class Inverst:
    def __init__(self, date, money, gz, kpow):
        self.date = date
        self.gz = gz
        self.money = money


fi = FundInv("162411", 100, startMoney=100, startShare=169.81)
fi.insert()
