from com_func.test_log import log
from com_func.confread import config
from jsonpath import jsonpath
from com_func.sql_request import mysql
from com_func.com_request_func import com_request, com_assertEqual, com_excel_read
import unittest
import ddt
import openpyxl


@ddt.ddt
class TestUpdate(unittest.TestCase):
    '''更新用户昵称'''
    Worksheet_name = "update"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        params = config.get("PRESET", "loan_params")
        respone = com_request(TestUpdate, "login", params=params)
        cls.token = "Bearer" + " " + jsonpath(respone, "$..token")[0]
        cls.member_id = jsonpath(respone, "$..id")[0]

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestUpdate, self.Worksheet_name, **kwargs, token=self.token)
            if kwargs["sql_cheack"]:  # 存在sql校验,获取更新后昵称
                res = mysql.sql_read(kwargs["sql_cheack"], self.member_id)
                print("实际昵称:", res["reg_name"])
                print("预期昵称:", self.params["reg_name"])
                self.assertEqual(res["reg_name"], self.params["reg_name"])  # 校验更新后的昵称与预期
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


@ddt.ddt
class TestInfo(unittest.TestCase):
    '''获取用户信息接口测试'''
    Worksheet_name = "info"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''随机获取用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        sql = "select id from futureloan.member where 1 order by rand() limit 10;"  # 截取一个已注册id
        res = mysql.sql_read(sql)
        cls.member_id = res["id"]

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestInfo, self.Worksheet_name, **kwargs)
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
