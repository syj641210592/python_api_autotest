import unittest
import ddt
import openpyxl
from com_func.test_log import log
from com_func.confread import config
from jsonpath import jsonpath
from com_func.sql_request import mysql
from com_func.com_request_func import com_request, com_assertEqual, com_excel_read
import decimal


@ddt.ddt
class TestInvest(unittest.TestCase):
    '''投资项目'''
    Worksheet_name = "invest"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录普通用户获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        params = config.get("PRESET", "loan_params")
        respone = com_request(TestInvest, "login", params=params)
        cls.token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
        cls.member_id = jsonpath(respone, "$..id")[0]
        cls.audit_loan = eval(config.get("SETUPDATA", "audit_loan"))
        cls.loan_id, cls.amount = cls.audit_loan["loan_id"], cls.audit_loan["amount"]

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            if kwargs["sql_cheack"]:  # 存在sql校验,获取投资的金额
                sql = "select leave_amount from futureloan.member where id=%s"
                leaveamount_b = mysql.sql_read(sql, self.member_id)["leave_amount"]  # 保留投资前的余额
                sql = "select count(*) from futureloan.financelog where pay_member_id=%s"
                count_b = mysql.sql_read(sql, self.member_id)["count(*)"]  # 保留投资前的条目数
            respone = com_request(TestInvest, self.Worksheet_name, **kwargs, token=self.token)
            if respone["code"] == 0:  # 当投资成功时减去已投资,不论预期是否成功
                TestInvest.amount -= int(self.params["amount"])
            com_assertEqual(self, respone, eval(kwargs["expect"]))
            if kwargs["sql_cheack"]:  # 存在sql校验,获取投资的金额
                sql = "select amount from futureloan.invest where id=%s"
                res = mysql.sql_read(sql, jsonpath(respone, "$..id"))
                self.assertEqual(decimal.Decimal(res["amount"]), decimal.Decimal(self.params["amount"]))  # 校验投资金额与预期
                sql = "select leave_amount from futureloan.member where id=%s"
                leaveamount_e = mysql.sql_read(sql, self.member_id)["leave_amount"]  # 保留投资后的余额
                self.assertEqual(leaveamount_b-leaveamount_e, decimal.Decimal(self.params["amount"]))  # 校验投资后条目数与预期
                sql = "select count(*) from futureloan.financelog where pay_member_id=%s"
                count_e = mysql.sql_read(sql, self.member_id)["count(*)"]  # 保留投资后的条目数
                self.assertEqual(count_e-count_b, 1)  # 校验条目数
        except AssertionError as e:
            log.error(f"用例--{info}--执行失败", exc_info=True)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "失败")
            raise e
        else:
            log.info(f"用例--{info}--执行成功", exc_info=False)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "成功")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.excel.wb.save(cls.excel.path)
        cls.excel.wb.close()


@ddt.ddt
class TestLoans(unittest.TestCase):
    '''投资项目'''
    Worksheet_name = "loans"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录普通用户获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        params = config.get("PRESET", "loan_params")
        respone = com_request(TestLoans, "login", params=params)
        cls.token = "Bearer" + " " + jsonpath(respone, "$..token")[0]

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestLoans, self.Worksheet_name, **kwargs, token=self.token)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
        except AssertionError as e:
            log.error(f"用例--{info}--执行失败", exc_info=True)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "失败")
            raise e
        else:
            log.info(f"用例--{info}--执行成功", exc_info=False)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "成功")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.excel.wb.save(cls.excel.path)
        cls.excel.wb.close()


