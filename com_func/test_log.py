import logging
from logging.handlers import TimedRotatingFileHandler
import os
from com_func.confread import config
from com_func.getpath import testpath


def logger_creat():
    # 创建log实例
    logger = logging.getLogger(__name__)

    # 设置输入信息等级
    logger.setLevel(config.get("LOGGING", "level"))

    # 设置日志输出格式
    mat = "%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s"
    logger_mat = logging.Formatter(mat)

    # 输出日志到文件
    handler_file = TimedRotatingFileHandler(os.path.join(testpath.LOG_DIR_PATH, config.get("FILE_NAME", "log")), when = "m", backupCount=3, encoding="utf-8")
    handler_file.setLevel(config.get("LOGGING", "file_level"))
    handler_file.setFormatter(logger_mat)

    # 输出日志到控制台
    handler_sh = logging.StreamHandler()
    handler_sh.setLevel(config.get("LOGGING", "stream_level"))
    handler_sh.setFormatter(logger_mat)

    # 加载logging
    logger.addHandler(handler_file)
    logger.addHandler(handler_sh)

    # 返回日志收集器
    return logger


log = logger_creat()