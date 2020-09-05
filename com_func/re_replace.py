from com_func.sql_request import mysql
from com_func.confread import config
import random
import re
from com_func.test_log import log


def params_get(params, cls, type_mode=0):
    '''处理带*参数'''
    try:
        if "*" in params:
            while re.search(r"\*(.+?\s.+?)\b", str(params)):
                res_value = re.search(r"\*(.+?\s.+?)\b", str(params))  # 获取带*参数
                res_str = res_value.group()
                res_list = res_value.group(1).split(" ")  # 切割带*参数
                if res_list[0] == "mobile_phone":
                    res = phone_create(res_list)
                elif res_list[0] == "member_id":
                    res = member_id_get(res_list, cls)
                elif res_list[0] == "amount":
                    res = leaveamount_get(res_list, cls)
                elif res_list[0] == "loan_id":
                    res = loan_id_get(res_list, cls)
                elif res_list[0] == "audit_loan":
                    res = audit_loan_get(res_list, cls)
                params = params.replace(res_str, str(res))
            mysql.con.commit()                       
    except Exception:  # 获取失败报判定错误
        log.error("带*参数解析失败", exc_info=True)
        raise AssertionError
    else:
        if type_mode == 0:
            return eval(params)
        else:
            return params


def phone_create(mark):
    '''替换*phone参数'''
    if "new" in mark:
        while True:
            phone = "156{:0<8}".format(random.randint(0, 99999999))  # 创建新号码
            sql = "select mobile_phone from futureloan.member where mobile_phone=%s;"
            res = mysql.sql_read(sql, phone)  # 执行sql语句
            if not res:  # 返回结果未None表示无该手机号码
                break
    elif "exist" in mark:
        phone = eval(config.get("PRESET", "loan_params"))["mobile_phone"]  # 提取一个已注册手机
    return phone


def member_id_get(mark, cls):
    '''替换*member参数'''
    if "exist" in mark:
        member_id = getattr(cls, mark[0])
    elif "new" in mark:
        while True:
            sql = "select id from futureloan.member where 1 order by rand() limit 10;"  # 截取一个已注册id
            res = mysql.sql_read(sql)
            if int(res["id"]) != int(getattr(cls, mark[0])):
                member_id = res["id"]  
                break
    elif "nuexist" in mark:
        sql = "select max(id) from futureloan.member;"  # 截取一个未注册id
        res = mysql.sql_read(sql)
        member_id = res["max(id)"] + 1
    elif "unadmin" in mark:
        member_id = eval(config.get("SETUPDATA", "params"))["mobile_phone"]
    elif "admin" in mark:
        member_id = eval(config.get("SETUPDATA", "admin_params"))["mobile_phone"]
    return member_id


def leaveamount_get(mark, cls):
    '''替换*amount参数'''
    if "over" in mark:
        sql = "UPDATE futureloan.member set leave_amount = 0 where id=%s;"  # 更新目标id的余额
        mysql.sql_read(sql, getattr(cls, "member_id"))  # 执行sql语句
        return getattr(cls, "leave_amount_max")


def loan_id_get(mark, cls):
    '''替换*loan_id参数'''
    if "exist" in mark:
        # sql = "select id from futureloan.loan where status=2 order by rand() limit 1;"  # 更新目标id的余额
        # res = mysql.sql_read(sql)
        # loan_id = res["id"]  # 截取一个竞标项目
        return getattr(cls, "loan_id")
    elif "pass" in mark:
        return getattr(cls, "loan_id_pass")
    elif "unbidding" in mark:
        sql = "select id from futureloan.loan where status = 3 order by rand() limit 1;"  # 截取一个非竞标项目
        res = mysql.sql_read(sql)
        member_id = res["id"]
        return member_id


def audit_loan_get(mark, cls):
    '''替换*audit_loan参数'''
    if "amount" in mark:
        audit_loan = getattr(cls, mark[1])
    elif "amountover" in mark:
        audit_loan = int(getattr(cls, "amount")) + 100
    return audit_loan
