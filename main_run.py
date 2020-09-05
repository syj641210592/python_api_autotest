from com_func.getpath import testpath
from com_func.confread import config
from com_func.sql_request import mysql
from com_func.env_func import env_params_init
import unittest
import unittestreport
import os

# 测试套件
test_suit = unittest.TestSuite()
# 测试加载器
test_loder = unittest.TestLoader()
# 加载加载器
test_suit.addTest(test_loder.discover(testpath.TEST_CASE_DIR_PATH))
# 预置环境账号
env_params_init()

if __name__ == "__main__":
    test_run = unittestreport.TestRunner(test_suit, tester="孙忘", desc="孙忘产生的测试报告", filename=os.path.join(testpath.REPORT_DIR_PATH, config.get("FILE_NAME", "report")))
    test_run.run()
    test_run.send_email("smtp.qq.com", 465, "641210592@qq.com", "bhcppjhdtmuhbfbe", "641210592@qq.com", True)
    mysql.con.close()