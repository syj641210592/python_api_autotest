import configparser
from com_func.getpath import testpath
import os

config = configparser.ConfigParser()
config.read(os.path.join(testpath.CONF_DIR_PATH, "conf.ini"), encoding="utf-8")


def config_write(section, option, value):
    '''写入配置文件'''
    if not isinstance(value, str):
        value = str(value)
    if not isinstance(option, str):
        option = str(option)
    if not config.has_section(section):  # 检查是否存在section
        config.add_section(section)
    if not config.has_option(section, option):  # 检查是否存在该option
        config.set(section, option, value)
    config.set(section, option, value)
    config.write(open(os.path.join(testpath.CONF_DIR_PATH, "conf.ini"), "w"))


if __name__ == "__main__":
    print(config.items("LOGGING"))