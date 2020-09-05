import os


class TestPath(object):

    def __init__(self):

        # 文件夹目录地址
        self.BASE_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 日志文件路径
        self.LOG_DIR_PATH = os.path.join(self.BASE_DIR_PATH, "logs") 

        # 报告文件路径
        self.REPORT_DIR_PATH = os.path.join(self.BASE_DIR_PATH, "report")

        # 用例数据目录
        self.TEST_CASE_DATA_DIR_PATH = os.path.join(self.BASE_DIR_PATH, "testdata")

        # 测试用例目录
        self.TEST_CASE_DIR_PATH = os.path.join(self.BASE_DIR_PATH, "testcase")

        # 配置文件目录
        self.CONF_DIR_PATH = os.path.join(self.BASE_DIR_PATH, "conf")


testpath = TestPath()