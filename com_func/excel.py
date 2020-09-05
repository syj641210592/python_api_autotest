import openpyxl
import os
from com_func.getpath import testpath
from com_func.confread import config


class ExcelOperate(object):
    '''操作excel'''

    def __init__(self, workbook):
        try:
            self.path = os.path.join(testpath.TEST_CASE_DATA_DIR_PATH, workbook)
            self.wb = openpyxl.load_workbook(self.path)
            self.shtname = self.wb.sheetnames
            self.id_clounm = config.get("EXCEL", "id_clounm")  # id列
            self.res_clounm = config.get("EXCEL", "res_clounm")  # 返回判断结果列
        except:
            print("工作簿加载失败")
            self.shtname = ""   

    def excel_read(self, worksheet):
        if self.excle_sheet_exist_check(worksheet):
            self.sht = self.wb[worksheet]
            self.data = self.excle_data_format(list(self.sht.rows))
            return self.data
        else:
            print("输入的sheet名不存在")
            return []

    def excel_write(self, worksheet, case_id, rng_value):
        if self.excle_sheet_exist_check(worksheet):
            self.sht = self.wb[worksheet]
            id_list = [i.value for i in self.sht[self.id_clounm]]
            id_index = id_list.index(case_id) + 1
            self.sht[self.res_clounm + str(id_index)].value = rng_value
        else:
            print("输入的sheet名不存在")

    def excle_sheet_exist_check(self, shtname):
        if shtname in self.shtname:
            return True
        else:
            return False

    @staticmethod
    def excle_data_format(data):
        data_list_format = []
        data_title = [i.value for i in data[0]]
        for data_value in data[1:]:
            data_value = [i.value for i in data_value]
            data_list_format.append(dict(zip(data_title, data_value)))
        return data_list_format
