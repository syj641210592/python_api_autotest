from com_func.confread import config
from com_func.re_replace import params_get
from com_func.excel import ExcelOperate
from com_func.handle_sign import HandleSign
import requests

def com_request(cls, api, **kwargs):
    '''通用请求方式'''
    # -------------------请求接口----------------------------
    api_url = config.get("URL", "url") + params_get(config.get("URL", api + "_url"), cls, 1)  # 登录接口请求地址

    # -------------------请求参数----------------------------
    params = params_get(str(kwargs["params"]).replace("\n", ""), cls)  # 参数处理
    setattr(cls, "params", params)
    method = config.get("METHOD", api + "_method")

    # -------------------请求头v2_v3----------------------------
    if method == "get":
        headers = eval(config.get("HEADERS", "headers"))
    else:
        headers = eval(config.get("HEADERS", "headers_v2"))  # v2
        # headers = eval(config.get("HEADERS", "headers_v3"))  # v3
    if "token" in kwargs.keys():
        headers["Authorization"] = kwargs["token"]  # v2
        # cryto_info = HandleSign.generate_sign(kwargs["token"].split(" ")[1])
        # params["timestamp"] = cryto_info["timestamp"]  # v3
        # params["sign"] = cryto_info["sign"]  # v3


    # -------------------请求响应----------------------------
    respone = requests.request(method, api_url, json=params, headers=headers)  # 请求
    return respone.json()


def com_assertEqual(self, respone, expect):
    '''判定'''
    print("实际状态:", dict(zip(["code", "msg"], [respone["code"], respone["msg"]])))
    print("预期状态:", expect)
    self.assertEqual(respone["code"], expect["code"])  # 判断code
    if "该标可投金额不足" in expect["msg"]:
        self.assertEqual(respone["msg"], expect["msg"].split(",")[0])  # msg
    else:
        self.assertEqual(respone["msg"], expect["msg"])  # msg


def com_excel_read(sheetname):
    workbook_name = config.get("EXCEL", "workbook_name")  # 工作簿名
    excel = ExcelOperate(workbook_name)  # 打开excel
    data_list = excel.excel_read(sheetname)  # 获取数据
    return excel, data_list
