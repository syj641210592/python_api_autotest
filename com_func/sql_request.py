import pymysql
from com_func.confread import config


class Mysql(object):
    '''链接数据库'''
    def __init__(self, host, port, user, password, charset):
        '''创建链接'''
        self.con = pymysql.connect(host=host, port=port, user=user, password=password, charset=charset)
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)

    def sql_read(self, sql, params="", mode="one"):
        if params == "":
            mysql.cur.execute(sql)
        else:
            mysql.cur.execute(sql, params)
        if mode == "one":
            res = self.cur.fetchone()
        else:
            res = self.cur.fetchall()
        self.con.commit()
        return res


mysql = Mysql(host=config.get("DB1", "url"),
                port=config.getint("DB1", "port"),
                user=config.get("DB1", "user"),
                password=config.get("DB1", "pwd"),
                charset=config.get("DB1", "charset"))

if __name__ == "__main__":
    sql = "select reg_name, mobile_phone from futureloan where mobile_phone like '156%'"
    res = mysql.sql_read(sql)
    print(res)
