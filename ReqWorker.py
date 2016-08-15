import logging
import sys
import traceback
from threading import Thread
from urllib.error import HTTPError

from fund import FundUtil


class ReqWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        logging.info("Thread is %s" % self.name)

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            # 从队列中获取任务并扩展tuple
            fund = self.queue.get()
            try:
                fund.dalprc = FundUtil.prices(fund.code)
                # fund.valuation = FundUtil.valuation(fund.code)[1]
                fund.valuation = sorted(fund.dalprc.items())[-1][1]
                # MongoUtil.insert(fund)
                print("%s---%s in %s" % (fund.code, fund.name, self.getName()))
            except HTTPError as err:
                # 是整型
                if err.code == 404:
                    logging.error("%s not found " % fund.code)
            except Exception as ex:
                print("%s!!!%s Unexpected error in %s:" % (fund.code, fund.name, self.getName()), sys.exc_info()[0])
                traceback.print_exc()
                self.queue.put((fund))
            finally:
                # 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
                self.queue.task_done()


if __name__ == "__main__":
    pass
