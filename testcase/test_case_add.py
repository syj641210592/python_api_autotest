from com_func.test_log import log
from com_func.confread import config
from jsonpath import jsonpath
from com_func.sql_request import mysql
from com_func.com_request_func import com_request, com_assertEqual, com_excel_read
import unittest
import ddt
import openpyxl


@ddt.ddt
class TestAdd(unittest.TestCase):
    '''新增项目'''
    Worksheet_name = "add"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        params = config.get("PRESET", "loan_params")
        respone = com_request(TestAdd, "login", params=params)
        cls.token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
        cls.member_id = jsonpath(respone, "$..id")[0]

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestAdd, self.Worksheet_name, **kwargs, token=self.token)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
            if kwargs["sql_cheack"]:  # 存在sql校验,获取新增项目名称
                res = mysql.sql_read(kwargs["sql_cheack"], jsonpath(respone, "$..id"))
                print("实际项目名称:", res["title"])
                print("预期项目名称:", self.params["title"])
                self.assertEqual(res["title"], self.params["title"])  # 校验更新后的昵称与预期
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
class TestAudit(unittest.TestCase):
    '''审核项目'''
    Worksheet_name = "audit"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录管理员账户获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        # ----------------管理员用户登录-------------------------
        params = config.get("PRESET", "admin_params")
        respone = com_request(TestAudit, "login", params=params)
        cls.admin_token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
        cls.admin_member_id = jsonpath(respone, "$..id")[0]
        # ----------------普通用户登录-------------------------
        params = config.get("PRESET", "loan_params")
        respone = com_request(TestAudit, "login", params=params)
        cls.token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
        cls.member_id = jsonpath(respone, "$..id")[0]
        
    def setUp(self):
        '''新增项目'''
        expect = {'code': 0, 'msg': 'OK'}  # 预期结果转换成字典
        params = str({
                    "member_id": self.member_id,
                    "title": "孙忘_财务自由1",
                    "amount": 1000000000,
                    "loan_rate": 1,
                    "loan_term": 1,
                    "loan_date_type": 1,
                    "bidding_days": 1
                    })  # 参数处理
        respone = com_request(TestAudit, "add", params=params, token=self.token)
        com_assertEqual(self, respone, expect)
        TestAudit.loan_id = jsonpath(respone, "$..id")[0]

    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestAudit, self.Worksheet_name, **kwargs, token=self.admin_token)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
            if kwargs["sql_cheack"]:  # 存在sql校验,获取审核项目状态
                res = mysql.sql_read(kwargs["sql_cheack"], self.loan_id)
                if self.params["approved_or_not"]:
                    statue = 2
                else:
                    statue = 5
                print("实际项目状态:", res["status"])
                print("预期项目状态:", statue)
                self.assertEqual(res["status"], statue)  # 校验更新后的状态与预期
                TestAudit.loan_id_pass = jsonpath(self.params, "$..loan_id")[0]
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

